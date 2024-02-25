import logging
import os
import sqlalchemy as sa
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, request, current_app, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_moment import Moment
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from bgben.config import Config
from flask_wtf.csrf import CSRFProtect
from elasticsearch import Elasticsearch
from flask_babel import Babel, lazy_gettext as _l
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from redis import Redis
import rq


# config stuff
mail=Mail()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'message'
login_manager.login_message = _l("请先进行登陆，再阅览您所要求的网页！")
moment = Moment()
ckeditor = CKEditor()
bootstrap = Bootstrap()
csrf = CSRFProtect()
babel = Babel()
admin = Admin(name='BGben')

# Admin
from bgben.models import User, Post, Tag, Comment, LikePost, LikeComment, Message, Notification, Contact, Newsletter, Task

admin_email = os.environ.get('ADMIN_EMAIL')

class UserView(ModelView):
  column_exclude_list = ('password_hashed')

  def is_accessible(self):
    if current_user == db.session.scalar(sa.select(User).where(User.email==admin_email)):
      return current_user.is_authenticated
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('main.home'))


class PostView(ModelView):
  can_delete = True
  can_create = False
  column_display_pk = True # optional, but I like to see the IDs in the list
  column_hide_backrefs = False
  column_list = ('id', 'title', 'subtitle', 'image_file', 'content', 'date_posted', 'user_id', 'active')


  def is_accessible(self):
    if current_user == db.session.scalar(sa.select(User).where(User.email==admin_email)):
      return current_user.is_authenticated
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('main.home'))


class TagView(ModelView):
  can_delete = True
  can_create = False
  column_display_pk = True # optional, but I like to see the IDs in the list
  column_hide_backrefs = False
  column_list = ('id', 'name', 'timestamp', 'user_id', 'posts', 'active')

  def is_accessible(self):
    if current_user == db.session.scalar(sa.select(User).where(User.email==admin_email)):
      return current_user.is_authenticated
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('main.home'))


class CommentView(ModelView):
  can_delete = True
  can_create = False
  column_display_pk = True # optional, but I like to see the IDs in the list
  column_hide_backrefs = False
  column_list = ('id', 'comment', 'date_posted', 'post_id', 'user_id', 'likes', 'active')

  def is_accessible(self):
    if current_user == db.session.scalar(sa.select(User).where(User.email==admin_email)):
      return current_user.is_authenticated
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('main.home'))


class LikePostView(ModelView):
  can_delete = True
  can_create = False
  column_display_pk = True # optional, but I like to see the IDs in the list
  column_hide_backrefs = False
  column_list = ('id', 'date_posted', 'user_id', 'post_id',)

  def is_accessible(self):
    if current_user == db.session.scalar(sa.select(User).where(User.email==admin_email)):
      return current_user.is_authenticated
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('main.home'))


class LikeCommentView(ModelView):
  can_delete = True
  can_create = False
  column_display_pk = True # optional, but I like to see the IDs in the list
  column_hide_backrefs = False
  column_list = ('id', 'date_posted', 'user_id', 'comment_id',)

  def is_accessible(self):
    if current_user == db.session.scalar(sa.select(User).where(User.email==admin_email)):
      return current_user.is_authenticated
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('main.home'))


class MessageView(ModelView):
  can_delete = True
  can_create = False
  column_display_pk = True # optional, but I like to see the IDs in the list
  column_hide_backrefs = False
  column_list = ('id', 'sender_id', 'recipient_id', 'body', 'timestamp', 'author_active', 'recipient_active')

  def is_accessible(self):
    if current_user == db.session.scalar(sa.select(User).where(User.email==admin_email)):
      return current_user.is_authenticated
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('main.home'))


class NotificationView(ModelView):
  can_delete = True
  can_create = False
  column_display_pk = True # optional, but I like to see the IDs in the list
  column_hide_backrefs = False
  column_list = ('id', 'name', 'user_id', 'timestamp', 'payload_json')

  def is_accessible(self):
    if current_user == db.session.scalar(sa.select(User).where(User.email==admin_email)):
      return current_user.is_authenticated
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('main.home'))


class ContactView(ModelView):
  can_delete = True
  can_create = False
  column_display_pk = True # optional, but I like to see the IDs in the list
  column_hide_backrefs = False
  column_list = ('id', 'name', 'email', 'category', 'content', 'timestamp')

  def is_accessible(self):
    if current_user == db.session.scalar(sa.select(User).where(User.email==admin_email)):
      return current_user.is_authenticated
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('main.home'))


class NewsletterView(ModelView):
  def is_accessible(self):
    if current_user == db.session.scalar(sa.select(User).where(User.email==admin_email)):
      return current_user.is_authenticated
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('main.home'))


class TaskView(ModelView):
  can_delete = True
  can_create = False
  column_display_pk = True # optional, but I like to see the IDs in the list
  column_hide_backrefs = False

  def is_accessible(self):
    if current_user == db.session.scalar(sa.select(User).where(User.email==admin_email)):
      return current_user.is_authenticated
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('main.home'))


class MyAdminIndexView(AdminIndexView):
  def is_accessible(self):
    if current_user == db.session.scalar(sa.select(User).where(User.email==admin_email)):
      return current_user.is_authenticated


admin.add_view(UserView(User, db.session))
admin.add_view(PostView(Post, db.session))
admin.add_view(TagView(Tag, db.session))
admin.add_view(CommentView(Comment, db.session))
admin.add_view(LikePostView(LikePost, db.session))
admin.add_view(LikeCommentView(LikeComment, db.session))
admin.add_view(MessageView(Message, db.session))
admin.add_view(NotificationView(Notification, db.session))
admin.add_view(ContactView(Contact, db.session))
admin.add_view(NewsletterView(Newsletter, db.session))
admin.add_view(TaskView(Task, db.session))


def get_locale():
  return request.accept_languages.best_match(current_app.config['LANGUAGES'])
  # return 'en'
  # return 'ja'
  # return 'zh'


def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  mail.init_app(app)
  migrate.init_app(app, db, render_as_batch=True)
  login_manager.init_app(app)
  moment.init_app(app)
  ckeditor.init_app(app)
  bootstrap.init_app(app)
  csrf.init_app(app)
  babel.init_app(app, locale_selector=get_locale)
  admin.init_app(app, index_view=MyAdminIndexView())

  from bgben.users.routes import users
  from bgben.posts.routes import posts
  from bgben.main.routes import main
  from bgben.errors.handlers import errors
  app.register_blueprint(users)
  app.register_blueprint(posts)
  app.register_blueprint(main)
  app.register_blueprint(errors)

  app.json.ensure_ascii = False

  app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None
  app.redis = Redis.from_url(app.config['REDIS_URL'])
  app.task_queue = rq.Queue('bgben-tasks', connection=app.redis)

  

  # error report
  if not app.debug:
    if app.config['MAIL_SERVER']:
      auth = None
      if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
      secure = None
      if app.config['MAIL_USE_TLS']:
        secure = ()
      mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr='no-reply@'+app.config['MAIL_SERVER'],
        toaddrs=app.config['ADMINS'][0], subject='BGben Failure',
        credentials=auth, secure=secure
      )
      mail_handler.setLevel(logging.ERROR)
      app.logger.addHandler(mail_handler)

      if not os.path.exists('logs'):
        os.mkdir('logs')
      file_handler = RotatingFileHandler('logs/bgben.log', maxBytes=10240,
                                         backupCount=10)
      file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
      ))
      file_handler.setLevel(logging.INFO)
      app.logger.addHandler(file_handler)

      app.logger.setLevel(logging.INFO)
      app.logger.info('Bgben startup')

  return app