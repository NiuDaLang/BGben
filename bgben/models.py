from datetime import datetime, timezone
from bgben import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from bgben.search import add_to_index, remove_from_index, query_index
from time import time
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
import json
import redis
import rq


class SearchableMixin(object):
  @classmethod
  def search(cls, expression):
    ids, total = query_index(cls.__tablename__, expression)
    
    if total == 0:
      return [], 0
    elif total['value'] == 0 or total == 0:
      return [], 0
    
    when = []
    for i in range(len(ids)):
      when.append((ids[i], i))
    query = sa.select(cls).where(cls.id.in_(ids)).where(cls.active == True).order_by(
      db.case(*when, value=cls.id)
    )
    return db.session.scalars(query), total
  
  @classmethod
  def before_commit(cls, session):
    session._changes = {
      'add': list(session.new),
      'update': list(session.dirty),
      'delete': list(session.deleted)
    }

  @classmethod
  def after_commit(cls, session):
    for obj in session._changes['add']:
      if isinstance(obj, SearchableMixin):
        add_to_index(obj.__tablename__, obj)
    for obj in session._changes['update']:
      if isinstance(obj, SearchableMixin):
        add_to_index(obj.__tablename__, obj)
    for obj in session._changes['delete']:
      if isinstance(obj, SearchableMixin):
        remove_from_index(obj.__tablename__, obj)
    session._changes = None

  @classmethod
  def reindex(cls):
    for obj in db.session.scalars(sa.select(cls)):
      add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


followers = sa.Table('followers',
                     db.metadata,
                     sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
                     sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True)
)


class User(UserMixin, SearchableMixin, db.Model):
  __searchable__=['username']
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  username: so.Mapped[str] = so.mapped_column(sa.String(10), unique=True, index=True)
  email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True, index=True)
  password_hashed: so.Mapped[str] = so.mapped_column(sa.String(192))
  image_file: so.Mapped[str] = so.mapped_column(sa.String(20), default='default.png')
  zodiac_sign: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), default='unknown')
  about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(360))
  account_created: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
  last_seen: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
  posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author', passive_deletes=True)
  comments: so.WriteOnlyMapped['Comment'] = so.relationship(back_populates='commenter', passive_deletes=True)
  post_likes: so.WriteOnlyMapped['LikePost'] = so.relationship(back_populates='post_liker', passive_deletes=True)
  comment_likes: so.WriteOnlyMapped['LikeComment'] = so.relationship(back_populates='comment_liker', passive_deletes=True)
  tags: so.WriteOnlyMapped['Tag'] = so.relationship(back_populates='tagger', passive_deletes=True)
  following: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers', passive_deletes=True
  )
  followers: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following', passive_deletes=True
  )
  messages_sent: so.WriteOnlyMapped['Message'] = so.relationship(foreign_keys='Message.sender_id', back_populates='author', passive_deletes=True)
  messages_received: so.WriteOnlyMapped['Message'] = so.relationship(foreign_keys='Message.recipient_id', back_populates='recipient', passive_deletes=True)
  last_message_read_time: so.Mapped[Optional[datetime]]
  notifications: so.WriteOnlyMapped['Notification'] = so.relationship(back_populates='user', passive_deletes=True)
  active: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=False, nullable=False)

  tasks: so.WriteOnlyMapped['Task'] = so.relationship(back_populates='user', passive_deletes=True)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.zodiac_sign}')"
  
  # Set Password
  def set_password(self, password):
    self.password_hashed = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hashed, password)
  
  # Registration Confirmation
  def get_registered(self):
    s = Serializer(current_app.config['SECRET_KEY'])
    return s.dumps({'user_id': self.id})
  
  @staticmethod
  def verify_register_token(token, expires_sec=1800):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
      user_id=s.loads(token, max_age=expires_sec)['user_id']
    except:
      return None
    
    return db.session.scalar(sa.select(User).where(User.id == user_id).where(User.active == False))

  # Reset Password
  def get_reset(self):
    s = Serializer(current_app.config['SECRET_KEY'])
    return s.dumps({'user_id': self.id})

  @staticmethod
  def verify_reset_token(token, expires_sec=1800):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
      user_id=s.loads(token, max_age=expires_sec)['user_id']
    except:
      return None
    
    return db.session.get(User, user_id)

  # Follow & Unfollow Users
  def follow(self, user):
    if not self.is_following(user):
      self.following.add(user)

  def unfollow(self, user):
    if self.is_following(user):
      self.following.remove(user)
  
  def is_following(self, user):
    query = self.following.select().where(User.id == user.id).where(User.active == True)
    return db.session.scalar(query) is not None
  
  def followers_count(self):
    query = sa.select(sa.func.count()).select_from(self.followers.select().where(User.active == True).subquery())
    return db.session.scalar(query)
  
  def following_count(self):
    query = sa.select(sa.func.count()).select_from(self.following.select().where(User.active == True).subquery())
    return db.session.scalar(query)

  def following_posts(self):
    Author = so.aliased(User)
    Follower = so.aliased(User)
    return (
      sa.select(Post)
      .join(Post.author.of_type(Author))
      .join(Author.followers.of_type(Follower), isouter=True)
      .where(sa.or_(
        Follower.id == self.id,
        Author.id == self.id,
      ))
      .where(Post.active == True)
      .group_by(Post)
      .order_by(Post.date_posted.desc())
    )
  
  def posts_count(self):
    query = sa.select(sa.func.count()).select_from(self.posts.select().where(Post.active == True).subquery())
    return db.session.scalar(query)
  
  # Messaging
  def unread_message_count(self):
    last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
    query = sa.select(Message).where(Message.recipient == self, Message.timestamp > last_read_time)
    return db.session.scalar(sa.select(sa.func.count()).select_from(query.subquery()))
  
  def add_notification(self, name, data):
    db.session.execute(self.notifications.delete().where(Notification.name == name))
    n = Notification(name=name, payload_json=json.dumps(data), user=self)
    db.session.add(n)
    return n

  # Redis Task
  def launch_task(self, name, description, *args, **kwargs):
    rq_job = current_app.task_queue.enqueue(f'bgben.tasks.{name}', self.id, *args, **kwargs)
    task = Task(id=rq_job.get_id(), name=name, description=description, user=self)
    db.session.add(task)
    return task
  
  def get_tasks_in_progress(self):
    query = self.tasks.select().where(Task.complete == False)
    return db.session.scalars(query)
  
  def get_task_in_progress(self, name):
    query = self.tasks.select().where(Task.name == name, Task.complete == False)
    return db.session.scalar(query)
  

@login_manager.user_loader
def load_user(user_id):
  return db.session.get(User, int(user_id))


tags_table = sa.Table('tags_association',
                      db.metadata,
                      sa.Column('post_id', sa.Integer, sa.ForeignKey('post.id'), primary_key=True),
                      sa.Column('tag_id', sa.Integer, sa.ForeignKey('tag.id'), primary_key=True)
)

class Post(SearchableMixin, db.Model):
  __searchable__=['title', 'subtitle']
  id: so.Mapped[int] = so.mapped_column(primary_key=True, index=True)
  title: so.Mapped[str] = so.mapped_column(sa.String(30))
  subtitle: so.Mapped[str] = so.mapped_column(sa.String(100))
  image_file: so.Mapped[str] = so.mapped_column(sa.String(20), default='post_default.jpg')
  content: so.Mapped[str] = so.mapped_column(sa.Text(50000))
  date_posted: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
  user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
  author: so.Mapped[User] = so.relationship(back_populates='posts')

  comments: so.Mapped[list['Comment']] = so.relationship(back_populates='commented_post', cascade='all, delete-orphan')
  likes: so.Mapped[list['LikePost']] = so.relationship(back_populates='liked_post', cascade='all, delete-orphan')
  
  tags: so.WriteOnlyMapped['Tag'] = so.relationship(
    secondary = tags_table, passive_deletes=True,
    cascade="all, delete", backref='posts'
  )

  active: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=True, nullable=False)


  def __repr__(self):
    return f"Post (id: {self.id}, title: {self.title}, date_posted: {self.date_posted})"
  
  def post_likes_count(self):
    query = sa.select(sa.func.count()).select_from(LikePost).where(LikePost.post_id == self.id)
    return db.session.scalar(query)
  
  def post_tags_count(self):
    query = sa.select(sa.func.count()).select_from(self.tags.select().where(Tag.active == True).subquery())
    return db.session.scalar(query)


class Tag(SearchableMixin, db.Model):
  __searchable__=['name']
  id: so.Mapped[int] = so.mapped_column(primary_key=True, index=True)
  name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
  timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
  user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
  tagger: so.Mapped[User] = so.relationship(back_populates='tags')
  active: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=True, nullable=False)

  def __repr__(self):
    return f"Tag: {self.name}, User_id={self.user_id}, Timestamp={self.timestamp}"


class Comment(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  comment: so.Mapped[str] = so.mapped_column(sa.String(250))
  date_posted: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
  user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
  commenter: so.Mapped[User] = so.relationship(back_populates='comments')
  
  post_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Post.id, ondelete='CASCADE'), nullable=False, index=True)
  commented_post: so.Mapped[Post] = so.relationship(back_populates='comments')
  likes: so.Mapped[list['LikeComment']] = so.relationship(back_populates='liked_comment', cascade='all, delete-orphan')
  active: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=True, nullable=False)


  def __repr__(self):
    return f"Comment.id {self.id} on Post No.{self.post_id}: {self.comment} by User No.{self.user_id}"
  
  def comment_likes_count(self):
    query = sa.select(sa.func.count()).select_from(LikeComment).where(LikeComment.comment_id == self.id)
    return db.session.scalar(query)


class LikePost(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  date_posted: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
  user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
  post_liker: so.Mapped[User] = so.relationship(back_populates='post_likes')
  
  post_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Post.id, ondelete='CASCADE'), nullable=False, index=True)
  liked_post: so.Mapped[Post] = so.relationship(back_populates='likes')

  def __repr__(self):
    return f"Post No.{self.post_id} was liked by User No.{self.user_id} "


class LikeComment(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  date_posted: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
  user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
  comment_liker: so.Mapped[User] = so.relationship(back_populates='comment_likes')
  
  comment_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Comment.id, ondelete='CASCADE'), nullable=False, index=True)
  liked_comment: so.Mapped[Comment] = so.relationship(back_populates='likes')

  def __repr__(self):
    return f"Comment No.{self.comment_id} was liked by User No.{self.user_id} "
  

class Message(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  sender_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
  recipient_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
  body: so.Mapped[str] = so.mapped_column(sa.String(140))
  timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
  author: so.Mapped[User] = so.relationship(foreign_keys='Message.sender_id', back_populates='messages_sent')
  author_active: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=True, nullable=True)
  recipient: so.Mapped[User] = so.relationship(foreign_keys='Message.recipient_id', back_populates='messages_received')
  recipient_active: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=True, nullable=True)

  def __repr__(self):
    return f'<Message>: {self.body}'
  

class Notification(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
  user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
  timestamp: so.Mapped[float] = so.mapped_column(index=True, default=time)
  payload_json: so.Mapped[str] = so.mapped_column(sa.Text)
  user: so.Mapped[User] = so.relationship(back_populates='notifications')

  def get_data(self):
    return json.loads(str(self.payload_json))
  

class Contact(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  name: so.Mapped[str] = so.mapped_column(sa.String(20))
  email: so.Mapped[str] = so.mapped_column(sa.String(120))
  category: so.Mapped[str] = so.mapped_column(sa.String(100), default='unknown')
  content: so.Mapped[str] = so.mapped_column(sa.String(500))
  timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=datetime.now(timezone.utc))
  junk: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=False, nullable=False)

  def __repr__(self):
    return f'<Contact from>: {self.name} on <Category>: {self.category}'


class Newsletter(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True, index=True)
  activated: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=False, nullable=False)
  active: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=False, nullable=False)
  timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=datetime.now(timezone.utc))

  def __repr__(self):
    return f'<Newsletter subscribed by>: {self.timestamp} on <Timestamp>: {self.timestamp}, activated: {self.activated}, active: {self.active}'

  # Registration Confirmation
  def get_registered(self):
    s = Serializer(current_app.config['SECRET_KEY'])
    return s.dumps({'subscriber_email': self.email})
  
  @staticmethod
  def verify_register_token(token, expires_sec=1800):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
      subscriber_email=s.loads(token, max_age=expires_sec)['subscriber_email']
    except:
      return None
    
    return db.session.scalar(sa.select(Newsletter).where(Newsletter.email == subscriber_email))


class Task(db.Model):
  id: so.Mapped[str] = so.mapped_column(sa.String(36), primary_key=True)
  name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
  description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))
  user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
  complete: so.Mapped[bool] = so.mapped_column(default=False)

  user: so.Mapped[User] = so.relationship(back_populates='tasks')
  
  def get_rq_job(self):
    try:
      rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
    except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
      return None
    return rq_job
  
  def get_progress(self):
    job = self.get_rq_job()
    return job.meta.get('progress', 0) if job is not None else 100
