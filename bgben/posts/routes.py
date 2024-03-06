import re, os, secrets
import sqlalchemy as sa
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, make_response, jsonify, current_app, send_from_directory
from bgben import db, get_locale
from bgben.posts.forms import (CreatePostForm, CommentForm)
from bgben.models import Post, Comment, LikePost, LikeComment, Tag, User
from flask_login import current_user, login_required
from bgben.posts.utils import save_picture, delete_picture  
from sqlalchemy import func
from flask_babel import _
from flask_ckeditor import upload_success, upload_fail


posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
  mode = 'create'
  form = CreatePostForm() 
  if form.validate_on_submit():
    picture_file = 'post_default.jpg'
    if form.main_picture.data:
      picture_file = save_picture(form.main_picture.data, 'static/post_pics', 800, 450)
    post = Post(
                title=form.title.data,
                subtitle=form.subtitle.data,
                image_file = picture_file,
                content=form.body.data,
                user_id=current_user.id,
                )
    if form.tags.data:
      for tag in form.tags.data:
        tag = tag.strip()
        if tag:
          post.tags.add(Tag(name=tag, user_id=current_user.id))
          
    db.session.add(post)
    db.session.commit()
    flash(_("投稿发布成功！"), "success")
    return redirect(url_for('posts.all_posts'))
  
  # Posts - Main Contents
  page = request.args.get('page', 1, type=int)
  user_posts = sa.select(Post).where(Post.user_id == current_user.id).where(Post.active == True).order_by(Post.date_posted.desc())
  posts = db.paginate(user_posts, page=page,
                      per_page=6, error_out=False)

  next_url = url_for('posts.new_post', username=current_user.username, page=posts.next_num) if posts.has_next else None
  prev_url = url_for('posts.new_post', username=current_user.username, page=posts.prev_num) if posts.has_prev else None

  ### Side bar ###
  # (1) Latest Posts
  ten_posts_query = sa.select(Post).where(Post.author == current_user).where(Post.active == True).order_by(Post.date_posted.desc()).limit(15)
  ten_posts = db.session.scalars(ten_posts_query)

  # (2) Monthly Posts
  month = sa.func.date_format(Post.date_posted, "%Y-%m").label(None)
  post_count = sa.func.count(Post.id).label(None)
  q = sa.select(month, post_count).order_by(Post.date_posted.desc()).group_by(sa.func.date_format(Post.date_posted, "%Y-%m")).where(Post.user_id==current_user.id).where(Post.active == True)

  monthly_posts_count = db.session.execute(q).all()

  # (3) Top tags
  user_tags = db.session.scalars(sa.select(Tag.name, func.count(Tag.name)).group_by(Tag.name).filter_by(user_id=current_user.id).order_by(Tag.timestamp.desc()).where(Tag.active == True))

  submit_value = _('投稿')
  return render_template('create_post.html', title=_('投稿'), form=form, legend=_('新稿子'), posts=posts, re=re, \
                         submit_value=submit_value, ten_posts=ten_posts, monthly_posts_count=monthly_posts_count, \
                          next_url=next_url, prev_url=prev_url, mode=mode, user_tags=user_tags)


@posts.route("/posts", methods=['GET'])
def all_posts():
  page = request.args.get('page', 1, type=int)
  posts = db.paginate(sa.select(Post).where(Post.active == True).order_by(Post.date_posted.desc()), page=page, per_page=6, error_out=False)

  # 20 Latest Posts
  twenty_posts = db.session.scalars(sa.select(Post).where(Post.active == True).order_by(Post.date_posted.desc()).limit(20))
  
  # Prolific Authors
  top_authors = db.session.scalars(sa.select(User).where(User.active == True).join(User.posts).group_by(User.id).order_by(func.count().desc()).limit(15))

  # Top tags
  tags = db.session.scalars(sa.select(Tag).where(Tag.active == True)).all()
  top_tags = []
  if len(tags) > 0:
    tag_count = sa.func.count(Tag.name).desc()
    q = (sa.select(Tag).group_by(Tag.name).where(Tag.active == True).order_by(tag_count))
    tags_sorted = db.session.scalars(q).all()
    if len(tags_sorted) < 11:
      top_tags = tags_sorted
    elif len(tags_sorted) >= 11:
      top_tags = tags_sorted[0:10]


  return render_template('posts.html', title=_('广场'), posts=posts, re=re, twenty_posts=twenty_posts, top_authors=top_authors, top_tags=top_tags)


@posts.route('/files/<path:filename>')
def uploaded_files(filename):
    # path = '/the/uploaded/directory'
    path = os.path.join(current_app.root_path, 'static/post_add_pics')
    return send_from_directory(path, filename)


@posts.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    # Add more validations here
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(f.filename)
    picture_fn = random_hex + f_ext

    # extension = f.filename.split('.')[-1].lower()
    if f_ext not in ['.jpg', '.gif', '.png', '.jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join(current_app.root_path, 'static/post_add_pics', picture_fn))
    url = url_for('posts.uploaded_files', filename=picture_fn)
    return upload_success(url, filename=picture_fn)  # return upload_success call


@posts.route("/post/<post_id>", methods=['GET', 'POST'])
def post(post_id):
  # No more message
  locale = get_locale()
  if locale == 'zh':
    comment_message = "您也说说感想吧！"
  elif locale == 'ja':
    comment_message = "あなたの考えも聞かせてね！"
  else:
    comment_message = "What say you?"

  # Post contents
  post= db.first_or_404(sa.select(Post).where(Post.id == post_id).where(Post.active == True))

  # If User liked This Post
  post_like = False
  if current_user.is_authenticated:
    post_like_query = sa.select(LikePost).where(LikePost.user_id == current_user.id, LikePost.post_id==post.id)
    post_like = db.session.scalar(post_like_query)

  # Make a Post Comment
  form=CommentForm()

  if form.validate_on_submit():
    comment = Comment(
                      comment = form.comment.data,
                      post_id = post.id,
                      user_id = current_user.id
                      )
    db.session.add(comment)
    db.session.commit()
    flash(_("评论发布成功！"), "success")
    return redirect(url_for('posts.post', post_id = post.id))
   
  # Get data for populating comments (Live Feed)
  comments = db.session.scalars(sa.select(Comment).where(Comment.post_id== post.id).where(Comment.active == True)).all()

  session['comments_db'] = []
  
  if comments is not None:
    for comment in comments:
      comment_likes = comment.comment_likes_count()
      comment_liked = False
      
      if current_user.is_authenticated:
        comment_liked_query = sa.select(LikeComment).where(LikeComment.user_id == current_user.id, LikeComment.comment_id == comment.id)
        comment_liked = db.session.scalar(comment_liked_query)

        if comment_liked:
          comment_liked = True
        else:
          comment_liked = False
        
      session['comments_db'].append([comment.id, comment.comment, comment.commenter.image_file, comment.commenter.username, 
                          comment.date_posted, comment_likes, comment_liked, comment.user_id])
  
  # Post Tags
  post_tags = db.session.scalars(post.tags.select()).all()

  ### Side bar ###
  author=post.author

  # (1) Latest Posts
  ten_posts_query = sa.select(Post).where(Post.author == author).where(Post.active == True).order_by(Post.date_posted.desc()).limit(15)
  ten_posts = db.session.scalars(ten_posts_query)

  # (2) Monthly Posts
  month = sa.func.date_format(Post.date_posted, "%Y-%m").label(None)
  post_count = sa.func.count(Post.id).label(None)
  q = sa.select(month, post_count).order_by(Post.date_posted.desc()).group_by(sa.func.date_format(Post.date_posted, "%Y-%m")).where(Post.user_id==current_user.id).where(Post.active == True)

  monthly_posts_count = db.session.execute(q).all()

  # (3) Top tags
  tags = db.session.scalars(sa.select(Tag.name, func.count(Tag.name)).group_by(Tag.name).filter_by(user_id=author.id).order_by(Tag.timestamp.desc()).where(Tag.active == True))
  return render_template('post.html', re=re, post=post, post_like=post_like, form=form, author=author, \
                         ten_posts=ten_posts, monthly_posts_count=monthly_posts_count, tags=tags, \
                         comment_message=comment_message, post_tags=post_tags, title=post.title)


@posts.route('/tag: <name>')
def tag(name):
  page = request.args.get('page', 1, type=int)
  tags_query = sa.select(Tag).where(Tag.name == name).where(Tag.active == True).order_by(Tag.timestamp.desc())
  tags = db.paginate(tags_query, page=page, per_page=3, error_out=False)
  next_url = url_for('posts.tag', name=name, page=tags.next_num) if tags.has_next else None
  prev_url = url_for('posts.tag', name=name, page=tags.prev_num) if tags.has_prev else None
                                         
  return render_template('tags.html', title=_('与%(name)s有关的笔记. ', name=name), tags=tags.items, next_url=next_url, prev_url=prev_url, re=re, name=name)


@posts.route('/monthly_posts/<user_id>/<month>')
def monthly_posts(user_id, month):
  page = request.args.get('page', 1, type=int)
  monthly_posts_query = sa.select(Post).where(func.date_format(Post.date_posted, "%Y-%m") == month, Post.user_id == user_id).where(Post.active == True)
  monthly_posts = db.paginate(monthly_posts_query, page=page, per_page=6, error_out=False)

  user = db.session.scalar(sa.select(User).where(User.id == user_id).where(User.active == True))

  query_month = sa.func.date_format(Post.date_posted, "%Y-%m").label(None)
  post_count = sa.func.count(Post.id).label(None)
  q = sa.select(query_month, post_count).order_by(Post.date_posted.desc()).group_by(sa.func.date_format(Post.date_posted, "%Y-%m")).where(Post.user_id==user.id).where(Post.active == True)

  monthly_posts_count = db.session.execute(q).all()
  
  next_url = url_for('posts.monthly_posts', user_id=user_id, month=month, page=monthly_posts.next_num) if monthly_posts.has_next else None
  prev_url = url_for('posts.monthly_posts', user_id=user_id, month=month, page=monthly_posts.prev_num) if monthly_posts.has_prev else None

  return render_template('monthly_posts.html', user=user, month=month, count=monthly_posts_count, monthly_posts=monthly_posts, next_url=next_url, prev_url=prev_url, re=re, title=_('%(username)s的月度笔记: %(month)s', username=user.username, month=month))


@posts.route("/like_post/<post_id>", methods=['POST'])
@login_required
def like_post(post_id):
  post = db.session.scalar(sa.select(Post).where(Post.id == post_id).where(Post.active == True))
  like_post = db.session.scalar(sa.select(LikePost).where(LikePost.user_id == current_user.id, LikePost.post_id == post.id))

  if not post:
    jsonify({"error": _("这篇笔记不存在！")}, 400)
  elif like_post:
    db.session.delete(like_post)
    db.session.commit()
  else:
    like_post = LikePost(
      user_id = current_user.id,
      post_id = post.id
    )
    db.session.add(like_post)
    db.session.commit()
  
  like_post = db.session.scalar(sa.select(LikePost).where(LikePost.user_id == current_user.id, LikePost.post_id == post.id))
  if like_post:
    like_post=True,
  else:
    like_post=False
  
  post_like_count = post.post_likes_count()
  return jsonify({"post_likes": post_like_count, "post_liked": like_post})


@posts.route("/like_comment/<int:comment_id>", methods=['POST'])
@login_required
def like_comment(comment_id):
  comment = db.session.scalar(sa.select(Comment).where(Comment.id == comment_id).where(Comment.active == True))
  like_comment = db.session.scalar(sa.select(LikeComment).where(LikeComment.user_id == current_user.id, LikeComment.comment_id == comment.id))

  if not comment:
    jsonify({"error": _("这条评论不存在！")}, 400)
  elif like_comment:
    db.session.delete(like_comment)
    db.session.commit()
  else:
    like_comment = LikeComment(
      user_id = current_user.id,
      comment_id = comment.id
    )
    db.session.add(like_comment)
    db.session.commit()
  
  like_comment = db.session.scalar(sa.select(LikeComment).where(LikeComment.user_id == current_user.id, LikeComment.comment_id == comment.id))

  if like_comment:
    comment_like_count = comment.comment_likes_count()
    return jsonify({"comment_likes": comment_like_count, "comment_liked": True})
  else:
    like_comment=False
    comment_like_count = comment.comment_likes_count()
    return jsonify({"comment_likes": comment_like_count, "comment_liked": False})


# Load comments one by one
@posts.route('/load_comments')
def load_comments():
  global comments_db
  comments_no = len(comments_db)

  if request.args:
    counter = int(request.args.get('c'))
    if counter == 0:
      res = make_response(jsonify(comments_db[0:comments_qty]), 200)
    elif counter == comments_no:
      res = make_response(jsonify({}), 200)
    else:
      res = make_response(jsonify(comments_db[counter: counter + comments_qty]), 200)
  
  return res


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
  mode = 'update'
  post = db.first_or_404(sa.select(Post).where(Post.id == post_id).where(Post.active == True))
  tags_count = post.post_tags_count()
  tags = db.session.scalars(post.tags.select()).all()

  if post.author != current_user:
    abort(403)
  form = CreatePostForm()
  if request.method == 'POST':
    if form.validate_on_submit():
      if tags:
        for tag in tags:
          db.session.delete(tag)
          db.session.commit()

      if form.main_picture.data:
        if post.image_file != 'post_default.jpg':
          old_pic_file = post.image_file
          delete_picture('static/post_pics', old_pic_file)
        picture_file = save_picture(form.main_picture.data, 'static/post_pics', 800, 450)
        post.image_file = picture_file

      post.title = form.title.data
      post.subtitle = form.subtitle.data
      post.content = form.body.data
      
      if form.tags.data:
        for tag in form.tags.data:
          tag = tag.strip()
          if tag != "":
            post.tags.add(Tag(name=tag, user_id=current_user.id))

      db.session.commit()
      flash(_('您的笔记已被更新!'), 'success')
      return redirect(url_for('posts.post', post_id=post_id))
    
  if request.method == 'GET':
    form.title.data = post.title
    form.subtitle.data = post.subtitle
    form.body.data = post.content
    
    if tags_count != 0:
      form.tags[0].data = tags[0].name

  ### Side bar ###
  # (1) Latest Posts
  ten_posts = db.session.scalars(sa.select(Post).where(Post.author == current_user).where(Post.active == True).order_by(Post.date_posted.desc()).limit(15))

  # (2) Monthly Posts
  month = sa.func.date_format(Post.date_posted, "%Y-%m").label(None)
  post_count = sa.func.count(Post.id).label(None)
  q = sa.select(month, post_count).order_by(Post.date_posted.desc()).group_by(sa.func.date_format(Post.date_posted, "%Y-%m")).where(Post.user_id==current_user.id).where(Post.active == True)

  monthly_posts_count = db.session.execute(q).all()

  # (3) Top tags
  user_tags = db.session.scalars(sa.select(Tag.name, func.count(Tag.name)).group_by(Tag.name).filter_by(user_id=current_user.id).order_by(Tag.timestamp.desc()).where(Tag.active == True))

  submit_value = _('更 新')
  return render_template('create_post.html', title=_('编辑笔记'), post=post, form=form, mode=mode, user_tags=user_tags,
                         tags_count=tags_count, tags=tags, ten_posts=ten_posts, monthly_posts_count=monthly_posts_count,
                         legend=_('编辑'), post_id=post.id, re=re, submit_value=submit_value )


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
  post = db.first_or_404(sa.select(Post).where(Post.id == post_id))

  if post.author != current_user:
    abort(403)

  # deactivate tags attached to the post
  tags = db.session.scalars(post.tags.select()).all()
  if tags:
    for tag in tags:
      tag.active = False
      db.session.commit()

  # delete pic file from static folder
  # if post.image_file != 'post_default.jpg':
  #   old_pic_file = post.image_file
  #   delete_picture('static/post_pics', old_pic_file)

  # deactivate post data from db
  post.active = False
  db.session.commit()
  flash(_('您的笔记已被删除!'), 'success')
  
  return redirect(url_for('users.user_page', username=current_user.username))


@posts.route("/edit_comment", methods=['POST'])
@login_required
def edit_comment():
  req = request.get_json()
  comment_id = req['comment_id']
  comment = db.session.get(Comment, comment_id)

  edited_comment = req['updated_comment']
  comment.comment = f'{edited_comment} (edited)'
  db.session.commit()

  saved_comment = db.session.get(Comment, comment_id).comment
  res = make_response(jsonify({"saved_edited_comment": saved_comment}), 200)

  return res


@posts.route("/delete_comment/<int:comment_id>", methods=['POST'])
@login_required
def delete_comment(comment_id):
  comment = db.session.get(Comment, comment_id)

  comment.active = False
  db.session.commit()

  comment = db.session.get(Comment, comment_id)


  if comment.active:
    comment = False
  else:
    comment = True
  return jsonify({"comment_deleted": comment} )