import re
import os
import json
import random
import sqlalchemy as sa
from flask import render_template, Blueprint, request, current_app, make_response, jsonify, g, url_for, redirect, flash, abort, session
from bgben import db, get_locale
from bgben.models import Post, Tag, User, Message, Notification, Contact, Newsletter
from bgben.users.forms import (EmptyForm, UnfollowForm)
from bgben.main.forms import SearchForm, MessageForm, ContactForm, CONTACT_CATEGORIES, DeleteForm, NewsletterForm
from bgben.main.utils import send_contact_confirm_email, send_message_email, send_newsletter_subscription_email
from sqlalchemy import func
from flask_login import current_user, login_required
from datetime import datetime, timezone
from flask_babel import _
from bgben import recaptcha


main = Blueprint('main', __name__)


@main.before_app_request
def before_request():
  if current_user.is_authenticated:
    current_user.last_seen = datetime.utcnow()
    db.session.commit()
  
  g.search_form = SearchForm()  
  g.locale = str(get_locale())



@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
  locale = get_locale()
  if locale == 'zh':
    theme = "灵魂的笔记本"
    starseed_test_memo = "星际种子：<br>从外星投胎到地球来帮助人类的灵魂✨"
  elif locale == 'ja':
    theme = "魂のメモ帳"
    starseed_test_memo = "スターシード：<br>他の惑星からやって来た魂✨"
  else:
    theme = "Memo Pad for the Souls"
    starseed_test_memo = "Starseed: souls originated from another planet✨"
  # 20 Latest Posts
  twenty_posts = db.session.scalars(sa.select(Post).where(Post.active == True).order_by(Post.date_posted.desc()).limit(20)).all()
  
  # Top tags
  count = func.count(Tag.name).label(None)
  query = (sa.select(Tag.name, count).group_by(Tag.name).where(Tag.active == True).order_by(count.desc()))
  tags_sorted = db.session.scalars(query).all()

  if len(tags_sorted) < 11:
    top_tags = tags_sorted
  elif len(tags_sorted) >= 11:
    top_tags = tags_sorted[0:10]

  # Latest Users
  users = db.session.scalars(sa.select(User).order_by(User.account_created.desc()).where(User.active == True).limit(10))

  # Newsletter Subscription Form
  form = NewsletterForm()
  if request.method == "POST":
    if form.validate_on_submit():
      nl_subscriber_email = form.email.data.strip()
      nl_subscriber = Newsletter(email=form.email.data.strip())
      db.session.add(nl_subscriber)
      db.session.commit()
      
      # get provisionally-registered subscriber
      nl_subscriber = db.session.scalar(sa.select(Newsletter).where(Newsletter.email == nl_subscriber_email))
      locale = get_locale()
      result = ""
      if send_newsletter_subscription_email(nl_subscriber):
        newsletterSubscribed = {
          'zh': f'我们向您的邮箱{nl_subscriber_email}发送了关于确认订阅的邮件，请在30分钟内查询并做出相应的反应。',
          'ja': f'ニュースレターの仮登録メールを{nl_subscriber_email}に送信しました。30分以内にご確認の返信をしてください。',
          'en': f'We have sent an email to {nl_subscriber_email}. Please confirm and respond within 30 minutes.'
        }
        result = newsletterSubscribed[locale]
        return jsonify({"result": "Success", "msg": result})
      else:
        newsletterSubError = {
        'zh': f'我们无法向您的邮箱{nl_subscriber_email}发送关于确认订阅的邮件。请确认邮箱地址并再次尝试！',
        'ja': f'{nl_subscriber_email} に送信を試みましたが、エラーとなりました。メールアドレスをご確認の上、後ほどもう一度お試しください。',
        'en': f'We were unable to send an email to {nl_subscriber_email}. Please check your email address and try again later!'
        }
        result = newsletterSubError[locale]
        return jsonify({"result": "Failure", "msg": result})
    else:
      return jsonify({"result":form.errors})
  return render_template("home.html", title=(_("主页")), re=re, twenty_posts=twenty_posts, top_tags=top_tags, 
                         starseed_test_memo=starseed_test_memo, users=users, form=form, theme=theme, sns="s")

@main.route('/starseed_result')
def starseed_result():
  result = request.args.get('r')
  starseedValuation = {
    'zh': {
          'a': "您更有可能是地球的原生灵魂。但是您挑战这项测试本身就证明了您是一个具有觉醒潜力的灵魂！",
          'b': "您对自己有可能是一颗星际种子的可能性有了一定的意识，但还需要进一步的苏醒。建议您在每天的生活中通过冥想等方式去继续寻找自己的根源！",
          'c': "您很可能是一颗带有特定使命的星际种子，已对自己来到地球的目的有了清晰的认知，并在积极采取行动唤醒更多的灵魂。欢迎您来一起分享您知道的阿卡西记录片段！"
          },
    'ja': {
          'a': "おそらくあなたは地球の魂である可能性が高いと思われます。しかし、あなたがこのテストに挑戦されたこと自体、あなたが目覚め得る魂であることの証です。",
          'b': "あなたは自分がスターシードであるのかもしれないと薄々気がついていますが、さらなる覚醒が必要です。日々の生活の中で瞑想などを通してご自分のルーツを探し続けることをお勧めします！",
          'c': "あなたはおそらく特定の使命を持って現れたスターシードで、地球上でのご自分の目標を明確に理解しており、より多くの魂を目覚めさせるために積極的に行動を起こしています。あなたが知っているアカシックレコードの1ページをぜひ共有しませんか？"
          },
    'en': {
          'a': "It seems more likely that you are a native soul of the earth. But the very fact that you challenge this test proves that you are an awakening soul!",
          'b': "You have some awareness of the possibility that you may be a starseed, but further awakening is needed. It is recommended that you continue this journey to the source by adopting various means such as meditation in your daily life!",
          'c': "You are most likely a starseed with a specific mission. You have a clear understanding of your purpose on earth and are actively taking actions to awaken more souls. You are welcome to share your unique piece of the Akashic Records!"
          }
  }
  
  locale = get_locale()
  result = starseedValuation[locale][result]

  res = make_response(jsonify({"result": result}), 200)

  return res


POST_SEARCH_QTY = 10
USER_SEARCH_QTY = 10
TAG_SEARCH_QTY = 20


@main.route('/search')
def search():
  if not g.search_form.validate():
    return redirect(url_for('main.home'))
  
  followform = EmptyForm()
  unfollowform = UnfollowForm()

  try:
    # Search Post
    posts_list = []
    posts_count = 0
    session['post_search_db'] = []

    posts, posts_total = Post.search(g.search_form.q.data)

    if posts_total != 0:
      posts_list = posts.all()
      posts_count = posts_total['value']
      for post in posts_list:
        session['post_search_db'].append([post.id, post.title, post.image_file, post.subtitle, post.author.username, post.author.image_file, post.date_posted])

    # Search User
    users_list = []
    users_count = 0
    session['user_search_db'] = []

    users, users_total = User.search(g.search_form.q.data)

    if users_total != 0:
      users_list = users.all()
      users_count = users_total['value']
      for user in users_list:
        current_user_is_authenticated = False
        user_following_current_user = False
        user_is_current_user = False
        current_user_following_user = False
        if current_user.is_authenticated:
          current_user_is_authenticated = True
          user = db.first_or_404(sa.select(User).where(User.username == user.username).where(User.active == True))
          if user.is_following(current_user):
            user_following_current_user = True
          if user == current_user:
            user_is_current_user = True
          if current_user.is_following(user):
            current_user_following_user = True
        session['user_search_db'].append([user.username, user.image_file, user.account_created, current_user_is_authenticated, user_following_current_user, user_is_current_user, current_user_following_user])

    # Search Tag
    tags_list = []
    tags_count = 0
    session['tag_search_db'] = []

    tags, tags_total = Tag.search(g.search_form.q.data)

    if tags_total != 0:
      tags_list = tags.all()
      for tag in tags_list:
        session['tag_search_db'].append(tag.name)
      session['tag_search_db'] = list(set(session['tag_search_db']))
      session['tags_count'] = len(session['tag_search_db'])
      tags_count = session['tags_count']

    return render_template('search.html', title=_('搜索结果'),\
                            re=re, followform=followform, unfollowform=unfollowform,\
                            posts_count=posts_count, users_count=users_count, tags_count=tags_count)
      
  except:
    posts_count = 0
    users_count = 0
    tags_count = 0

    return render_template('search.html', title=_('搜索结果'), re=re, followform=followform, unfollowform=unfollowform, posts_count=posts_count, users_count=users_count, tags_count=tags_count)


# Load post_search_result one by one
@main.route('/load_post_search_result')
def load_post_search_result():
  post_search_result_no = len(session['post_search_db'])

  if request.args:
    counter = int(request.args.get('p'))
    if counter == 0:
      res = make_response(jsonify(session['post_search_db'][0:POST_SEARCH_QTY]), 200)
    elif counter == post_search_result_no:
      res = make_response(jsonify({}), 200)
    else:
      res = make_response(jsonify(session['post_search_db'][counter: counter + POST_SEARCH_QTY]), 200)
  
  return res


# Load user_search_result one by one
@main.route('/load_user_search_result')
def load_user_search_result():
  user_search_result_no = len(session['user_search_db'])

  if request.args:
    counter = int(request.args.get('u'))
    if counter == 0:
      res = make_response(jsonify(session['user_search_db'][0:USER_SEARCH_QTY]), 200)
    elif counter == user_search_result_no:
      res = make_response(jsonify({}), 200)
    else:
      res = make_response(jsonify(session['user_search_db'][counter: counter + USER_SEARCH_QTY]), 200)
  
  return res


# Load tag_search_result one by one
@main.route('/load_tag_search_result')
def load_tag_search_result():
  tag_search_result_no = len(session['tag_search_db'])

  if request.args:
    counter = int(request.args.get('t'))
    if counter == 0:
      res = make_response(jsonify(session['tag_search_db'][0:TAG_SEARCH_QTY]), 200)
    elif counter == tag_search_result_no:
      res = make_response(jsonify({}), 200)
    else:
      res = make_response(jsonify(session['tag_search_db'][counter: counter + TAG_SEARCH_QTY]), 200)
  
  return res


@main.route("/starseed_test")
def starseed_test():
  locale = get_locale()
  if locale == 'zh':
    with open(os.path.join(current_app.static_folder, 'data/starseed_test_file.json'), 'r') as file:
      starseed_tests = json.load(file)['zh']
  elif locale == 'ja':
    with open(os.path.join(current_app.static_folder, 'data/starseed_test_file.json'), 'r') as file:
      starseed_tests = json.load(file)['ja']
  else:
    with open(os.path.join(current_app.static_folder, 'data/starseed_test_file.json'), 'r') as file:
      starseed_tests = json.load(file)['en']

  test_list = list(starseed_tests.items())
  random_test = random.choice(test_list)[1]
  return make_response(jsonify({"selected_test": random_test}), 200)


@main.route('/user/<username>/popup')
def user_popup(username):
  user = db.first_or_404(sa.select(User).where(User.username == username).where(User.active == True))

  followform = EmptyForm()
  unfollowform = UnfollowForm()

  return render_template('user_popup.html', user=user, followform=followform, unfollowform=unfollowform)


@main.route('/user/<username>/following')
def following_list(username):
  user = db.first_or_404(sa.select(User).where(User.username == username).where(User.active == True))
  followings = db.session.scalars(user.following.select().where(User.active == True)).all()

  followform = EmptyForm()
  unfollowform = UnfollowForm()

  return render_template('following.html', title=_('%(user)s的关注名单', user = user.username), user=user, followings=followings, re=re, followform=followform, unfollowform=unfollowform)


@main.route('/user/<username>/followers')
def followers(username):
  user = db.first_or_404(sa.select(User).where(User.username == username).where(User.active == True))
  followers = db.session.scalars(user.followers.select().where(User.active == True)).all()

  followform = EmptyForm()
  unfollowform = UnfollowForm()

  return render_template('followers.html', title=_('%(user)s的粉丝名单', user = user.username), user=user, followers=followers, 
                         re=re, followform=followform, unfollowform=unfollowform)


@main.route('/send/message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
  user = db.first_or_404(sa.select(User).where(User.username == recipient).where(User.active == True))
  
  form = MessageForm()
  if form.validate_on_submit():
    msg = Message(author=current_user, recipient=user, body=form.message.data)
    db.session.add(msg)
    user.add_notification('unread_message_count', user.unread_message_count())
    db.session.commit()

    send_message_email(user, current_user, content=form.message.data)
    flash(_('您的信息已发出！'))
    return redirect(url_for('main.messages', username=current_user.username, tab='out'))
  
  return render_template('send_message.html', title=_('发信息'), form=form, recipient=recipient, re=re)


IN_MSGS_QTY = 10
OUT_MSGS_QTY = 10


@main.route('/messages/<username>/<tab>')
@login_required
def messages(username, tab='in'):
  user = db.first_or_404(sa.select(User).where(User.username == username).where(User.active == True))
  if user == current_user:
    form=DeleteForm()
    current_user.last_message_read_time = datetime.now(timezone.utc)
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()

    # Get in_msgs for populating in_msgs (Live Feed)
    in_msgs_query = current_user.messages_received.select().where(Message.recipient_active==True).order_by(Message.timestamp.desc())
    out_msgs_query = current_user.messages_sent.select().where(Message.author_active==True).order_by(Message.timestamp.desc())
    in_msgs = db.session.scalars(in_msgs_query).all()
    out_msgs = db.session.scalars(out_msgs_query).all()

    session['in_msgs_db'] = []
    
    if in_msgs is not None:
      for in_msg in in_msgs:
        session['in_msgs_db'].append([in_msg.id, in_msg.author.username, in_msg.author.image_file, in_msg.body, in_msg.timestamp])

    session['out_msgs_db'] = []
    
    if out_msgs is not None:
      for out_msg in out_msgs:
        session['out_msgs_db'].append([out_msg.id, out_msg.recipient.username, out_msg.recipient.image_file, out_msg.body, out_msg.timestamp])

  return render_template('messages.html', re=re, form=form, user=user, title=_('私信邮箱'), in_msgs=in_msgs, out_msgs=out_msgs, tab=tab)


# Load in_msgs one by one
@main.route('/load_in_msgs')
def load_in_msgs():
  in_msg_no = len(session['in_msgs_db'])

  if request.args:
    counter = int(request.args.get('i'))
    if counter == 0:
      res = make_response(jsonify(session['in_msgs_db'][0:IN_MSGS_QTY]), 200)
    elif counter == in_msg_no:
      res = make_response(jsonify({}), 200)
    else:
      res = make_response(jsonify(session['in_msgs_db'][counter: counter + IN_MSGS_QTY]), 200)
  
  return res


@main.route('/load_out_msgs')
def load_out_msgs():
  out_msg_no = len(session['out_msgs_db'])

  if request.args:
    counter = int(request.args.get('o'))
    if counter == 0:
      res = make_response(jsonify(session['out_msgs_db'][0:OUT_MSGS_QTY]), 200)
    elif counter == out_msg_no:
      res = make_response(jsonify({}), 200)
    else:
      res = make_response(jsonify(session['out_msgs_db'][counter: counter + OUT_MSGS_QTY]), 200)
  
  return res


@main.route('/notifications')
@login_required
def notifications():
  since = request.args.get('since', 0.0, type=float)
  query = current_user.notifications.select().where(Notification.timestamp > since).order_by(Notification.timestamp.asc())
  notifications = db.session.scalars(query)
  return [{
    'name': n.name,
    'data': n.get_data(),
    'timestamp': n.timestamp
  } for n in notifications]


@main.route('/about')
def about():
  return render_template('about.html', re=re, title=_('关于BGben'),)


@main.route('/user_policy')
def user_policy():
  return render_template('user_policy.html', re=re, title=_('利用规则'),)


@main.route('/privacy_policy')
def privacy_policy():
  return render_template('privacy_policy.html', re=re, title=_('隐私政策'),)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm(category='default')
  if request.method == 'POST':
    if not recaptcha.verify():
      flash('Error ReCaptcha')
      return redirect(url_for('main.contact'))
    elif form.validate_on_submit():
      contact = Contact(
        name = form.name.data,
        email = form.email.data.strip(),
        category = form.category.data,
        content = form.content.data
      )
      db.session.add(contact)
      db.session.commit()
      category = dict(CONTACT_CATEGORIES).get(form.category.data)
      flash(_('谢谢您发出的信号，我们将尽快回复！'))
      send_contact_confirm_email(form.name.data, form.email.data.strip(), category, form.content.data)
      return redirect(url_for('main.contact'))
  return render_template('contact.html', title=_('联系管理人'), form=form, re=re)


@main.route('/faq')
def faq():
  return render_template('faq.html', re=re, title=_('常见问题'),)


@main.route("/message/<int:message_id>/delete_received_message", methods=['POST'])
@login_required
def delete_received_message(message_id):
  msg = db.session.get(Message, message_id)
    
  if msg.recipient != current_user:
    abort(403)

  # deactivate message data from db
  msg.recipient_active = False
  db.session.commit()
  
  msg = db.session.get(Message, message_id)

  if msg.recipient_active:
    msg = False
  else:
    msg = True

  return jsonify({"received_msg_deleted": msg})


@main.route("/message/<int:message_id>/delete_sent_message", methods=['POST'])
@login_required
def delete_sent_message(message_id):
  msg = db.session.get(Message, message_id)

  if msg.author != current_user:
    abort(403)

  # deactivate message data from db
  msg.author_active = False
  db.session.commit() 
  
  msg = db.session.get(Message, message_id)

  if msg.author_active:
    msg = False
  else:
    msg = True

  return jsonify({"sent_msg_deleted": msg})


@main.route("/nl_sub_confirm/<token>")
def nl_sub_confirm(token):
  new_subscriber = Newsletter.verify_register_token(token)
  if new_subscriber is None:
    flash(_('此密码链接无效或已失效，请再次尝试！'), 'danger')
    return redirect(url_for('main.home'))
  else:
    new_subscriber.activated = True
    db.session.commit()
    flash(_('恭喜！您成功订阅啦! 您的邮箱：%(email)s', email=new_subscriber.email), 'success' )
    return redirect(url_for('main.home'))
  

@main.route("/export_posts")
@login_required
def export_posts():
  if current_user.get_task_in_progress('export_posts'):
    flash(_('有一项导出任务正在进行中。。。'))
  else:
    current_user.launch_task('export_posts', _('数据输出完成度...'))
    db.session.commit()
  return redirect(url_for('users.account', username=current_user.username))

