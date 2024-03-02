import time
import sys
import sqlalchemy as sa
import json
from rq import get_current_job
from bgben import create_app, db
from bgben.models import Task, User, Post
from flask import render_template
from bgben.email import send_email
from flask_babel import _


app = create_app()
app.app_context().push()


def example(seconds):
  job = get_current_job()
  for i in range(seconds):
    job.meta['progress'] = 100.0 * i / seconds
    job.save_meta()
    time.sleep(1)
  job.meta['progress'] = 100
  job.save_meta()


def _set_task_progress(progress):
  job = get_current_job()
  if job:
    job.meta['progress'] = progress
    job.save_meta()
    task = db.session.get(Task, job.get_id())
    task.user.add_notification('task_progress', {'task_id': job.get_id(),
                                                 'progress': progress})
    if progress >= 100:
      task.complete = True
    db.session.commit()


def export_posts(user_id):
  try:
    user = db.session.get(User, user_id)
    _set_task_progress(0)
    data = []
    i = 0
    total_posts_count = db.session.scalar(sa.select(sa.func.count()).select_from(user.posts.select().subquery()))
    
    total_posts = db.session.scalars(user.posts.select().order_by(Post.date_posted.asc()))
    for post in total_posts:
       data.append({'主题/title/タイトル': post.title,
                    '副主题/subtitle/サブタイトル': post.subtitle,
                    '笔记内容/body/本文': post.content,
                    '发布日期/date_posted/投稿日': post.date_posted.isoformat() + 'Z'})
       time.sleep(5)
       i += 1
       _set_task_progress(100 * i // total_posts_count)
    
    send_email(
      '您的[BGben]笔记档案！ / Your [BGben] Posts! / あなたの[BGben]アーカイブです！',
      sender=app.config['ADMINS'][0],
      recipients=[user.email],
      text_body=render_template('email/export_posts.txt', user=user),
      html_body=render_template('email/export_posts.html', user=user),
      attachments=[('posts.json', 'application/json', json.dumps({'posts': data}, indent=4))],
      sync=True,
    )
  except Exception:
    _set_task_progress(100)
    app.logger.error('Unhandled exception', exc_info=sys.exc_info)
  finally:
    _set_task_progress(100)

