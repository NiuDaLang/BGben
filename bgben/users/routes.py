import re, os, json
import sqlalchemy as sa
from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app, make_response, jsonify, session
from bgben import db, get_locale
from bgben.users.forms import (RegistrationForm, LoginForm, TestPassForm, UpdateAccountForm, 
                         RequestResetForm, ResetPasswordForm, EmptyForm, UnfollowForm)
from bgben.models import User, Post, Tag
from flask_login import login_user, current_user, logout_user, login_required
from bgben.users.utils import save_picture, delete_picture, send_reset_email, send_registration_email, set_test_pass_session, pop_test_pass_session
from sqlalchemy import func
from flask_babel import _
from urllib.parse import urlsplit


users = Blueprint('users', __name__)


@users.route("/register_test_quiz", methods=['GET', 'POST'])
def register_test_quiz():
  req = request.get_json()
  selection = req['selection']

  locale = get_locale()
  if locale == 'zh':
    with open(os.path.join(current_app.static_folder, 'data/register_quiz.json'), 'r') as file:
      selected_questions = json.load(file)['zh'][selection]
  elif locale == 'ja':
    with open(os.path.join(current_app.static_folder, 'data/register_quiz.json'), 'r') as file:
      selected_questions = json.load(file)['ja'][selection]
  else:
    with open(os.path.join(current_app.static_folder, 'data/register_quiz.json'), 'r') as file:
      selected_questions = json.load(file)['en'][selection]

  return make_response(jsonify({"selected_questions": selected_questions}), 200)


@users.route("/register_test", methods=['GET', 'POST'])
def register_test():
  lang = get_locale()
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  
  form = TestPassForm()
  return render_template("register-test.html", form=form, re=re, title=_("注册测试"), lang=lang)


@users.route("/register_test_pass", methods=['POST'])
def register_test_pass():
  form = TestPassForm()
  if form.validate_on_submit():
    set_test_pass_session()
    return redirect(url_for('users.register'))
  else:
    return redirect(url_for('main.home'))

@users.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))

  if "test_pass" in session and session['test_pass'] == True:
    form = RegistrationForm()
    if form.validate_on_submit():
      user = User(username=form.username.data, email=form.email.data.strip())
      user_email = form.email.data.strip()
      user.set_password(form.password.data)
      db.session.add(user)
      db.session.commit()

      # clean form fields
      form.username.data = ""
      form.email.data = ""
      form.agree.data = False
      # get provisionally-registered user
      user = db.session.scalar(sa.select(User).where(User.email == user_email))

      if send_registration_email(user):
        flash(_('我们向您的邮箱%(email)s发送了关于确认账户注册的邮件，请在30分钟内查询并激活您的账户。如果您找不到邮件的话，请查看您的垃圾邮箱，或直接通过本网站页脚的"联系管理人"链接联系我们。', email=user_email), 'success' )
        pop_test_pass_session()
        return redirect(url_for('main.home'))
      else:
        flash(_('我们试图向您的邮箱%(email)s发送邮件，但是失败了。请确认邮箱地址是否正确并再次尝试注册！', email=user_email), 'success' )
  else:
    return redirect(url_for('users.register_test'))

  return render_template("register.html", title=_("注册"), form=form, re=re)


@users.route("/first_login/<token>", methods=['GET', 'POST'])
def first_loin(token):
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  user = User.verify_register_token(token)
  if user is None:
    flash(_('此密码链接无效或已失效，请再次尝试！'), 'danger')
    return redirect(url_for('users.register_test'))
  else:
    user.active = True
    db.session.commit() 
    flash(_('恭喜%(username)s, 您成功注册啦！', username=user.username), 'success' )
  return redirect(url_for('users.login'))


@users.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  form = LoginForm()
  if form.validate_on_submit():
      user = db.session.scalar(sa.select(User).where(User.email==form.email.data.strip()).where(User.active == True))
      
      if user and user.active and user.check_password(form.password.data):
        login_user(user, remember=form.remember.data)
        # e.g. if accessing from /account directrly without logging in
        next_page = request.args.get('next')
        flash(_('欢迎回来，%(user)s!', user=user.username), 'login-success')
        if not next_page or urlsplit(next_page).netloc != '':
          next_page = url_for('main.home')
        return redirect(next_page)
      elif user and not user.active and user.check_password(form.password.data):
        flash(_('本账号已被停用，如有问题请联系管理人！'), 'danger')
      else:
        flash(_('登陆不成功，请再次确认注册邮箱及密码！'), 'danger')

  return render_template("login.html", title=_("登陆"), form=form, re=re)


@users.route("/logout")
def logout():
  logout_user()
  flash(_('您已经退出了系统，再来玩哦！'), 'message')
  return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()

  if form.validate_on_submit():
    if form.picture.data:
      if current_user.image_file != 'default.png':
        old_pic_file = current_user.image_file
        delete_picture('static/profile_pics', old_pic_file)
      picture_file = save_picture(form.picture.data, 'static/profile_pics', 300, 300)
      current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data.strip()
    current_user.zodiac_sign = form.zodiac_sign.data
    current_user.about_me = form.about_me.data
    db.session.commit()
    flash(_('您的设置内容已被更新！'), 'success')
    # use redirect rather than render_template, to avoid re-post of the form 
    # (apply GET request here)
    return redirect(url_for('users.account'))
  elif request.method == 'GET':
    form.zodiac_sign.default = current_user.zodiac_sign
    form.process()
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.about_me.data = current_user.about_me
  image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
  zodiac_file = url_for('static', filename='zodiac_signs/' + current_user.zodiac_sign + '.png')
  return render_template('account.html', title=_('账户设置'), image_file=image_file, form=form, zodiac_file=zodiac_file, re=re)


@users.route("/user/<string:username>")
def user_page(username):
  page=request.args.get('page', 1, type=int)

  if current_user.is_authenticated and current_user.username == username:
    user=current_user
    posts = db.paginate(current_user.following_posts(),
      page=page, per_page=12
    )
  else:
    user=db.first_or_404(sa.select(User).where(User.username == username).where(User.active == True))

    posts = db.paginate(sa.select(Post).where(Post.author == user).where(Post.active == True).order_by(Post.date_posted.desc()),
                        page=page, per_page=6, error_out=False)
  
  user_tags = db.session.query(Tag.name, func.count(Tag.name)).group_by(Tag.name).filter_by(user_id=user.id).where(Tag.active == True).order_by(Tag.timestamp.desc())

  ten_posts = db.session.scalars(user.posts.select().where(Post.active == True).order_by(Post.date_posted.desc()).limit(10)).all()

  next_url = url_for('users.user_page', username=user.username, page=posts.next_num) if posts.has_next else None
  prev_url = url_for('users.user_page', username=user.username, page=posts.prev_num) if posts.has_prev else None
  followform = EmptyForm()
  unfollowform = UnfollowForm()

  # Monthly Posts
  month = sa.func.strftime("%Y-%m", Post.date_posted).label(None)
  post_count = sa.func.count(Post.id).label(None)
  q = sa.select(month, post_count).order_by(Post.date_posted.desc()).group_by(sa.func.strftime("%Y-%m", Post.date_posted)).where(Post.user_id==user.id).where(Post.active == True)
  monthly_posts_count = db.session.execute(q).all()

  # User Posts Count
  posts_count_query = sa.select(sa.func.count()).select_from(user.posts.select().where(Post.active == True).subquery())
  posts_count = db.session.scalar(posts_count_query)

  return render_template('user_posts.html', user=user, posts=posts, re=re, next_url=next_url, prev_url=prev_url, \
                         title=(_("%(user)s的动态", user=user.username)), followform=followform, unfollowform=unfollowform, posts_count=posts_count,\
                         monthly_posts_count=monthly_posts_count, ten_posts=ten_posts, user_tags=user_tags)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  form = RequestResetForm()
  if form.validate_on_submit():
    user=db.session.scalar(sa.select(User).where(User.email == form.email.data.strip()).where(User.active == True))
    if user:
      send_reset_email(user)
      flash(_('我们向您的邮箱发送了关于密码重置方法的邮件，请在30分钟内查询并进行操作。'), 'success')
      return redirect(url_for('users.login'))
  return render_template('request_reset.html', title=_('我要重置密码'), form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  user = User.verify_reset_token(token)
  if user is None:
    flash(_('此密码链接无效或已失效，请再次尝试！'), 'danger')
    return redirect(url_for('users.reset_request'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    user.set_password(form.password.data)
    db.session.commit()
    flash(_('您的密码被重置了，现在可以登陆了！'), 'success')
    return redirect(url_for('users.login'))
  return render_template('reset_token.html', title=_('重置密码'), form=form)


@users.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
  form = EmptyForm()
  if form.validate_on_submit():
    user = db.session.scalar(sa.select(User).where(User.username == username).where(User.active == True))

    if user is None:
      flash(_('%(username)s不是BGben用户哦！', username=username) )
      return redirect(url_for('main.home'))
    if user == current_user:
      flash(_('自己无法关注自己哦！'))
      return redirect(url_for('users.user_page', user=user))
    current_user.follow(user)
    db.session.commit()
    flash(_('您正在关注%(username)s', username=username))
    return redirect(url_for('users.user_page', username=user.username))
  else:
    return redirect(url_for('home'))
  

@users.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
  form = EmptyForm()
  if form.validate_on_submit():
    user = db.session.scalar(sa.select(User).where(User.username == username).where(User.active == True))

    if user is None:
      flash(_('%(username)s不是BGben用户哦！', username=username))
      return redirect(url_for('main.home'))
    if user == current_user:
      flash(_('自己无法取消关注自己哦！'))
      return redirect(url_for('users.user_page', username=user.username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('您已经取消对%(username)s的关注！', username=username))
    return redirect(url_for('users.user_page', username=user.username))
  else:
    return redirect(url_for('main.home'))
  