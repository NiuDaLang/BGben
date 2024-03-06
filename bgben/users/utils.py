import os
import secrets
from PIL import Image
from flask import url_for, current_app, render_template, session
from flask_babel import _
from bgben.email import send_email


def set_test_pass_session():
  session['test_pass'] = True


def pop_test_pass_session():
  session.pop('test_pass', None)


def save_picture(form_picture, pic_folder, width, height):
  random_hex = secrets.token_hex(8)
  # _, f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + '.png'
  picture_path = os.path.join(current_app.root_path, pic_folder, picture_fn)

  output_size = (width, height)
  i = Image.open(form_picture)
  i.thumbnail(output_size)
  i.save(picture_path)

  return picture_fn


def delete_picture(pic_folder, picture_fn):
  os.remove(os.path.join(current_app.root_path, pic_folder, picture_fn))


def send_registration_email(user):
    token = user.get_registered()
    link = url_for('users.first_loin', token=token, _external=True)

    pic_attachments = [{
        'folder_path': 'bgben/static/images',
        'filename': 'BGben_logo1.png',
        'content_type': 'image/png',
        'disposition': 'inline',
        'content-ID': '<BgbenLogo>'
    }]

    send_email(_('欢迎申请[BGben]用户账号，请在30分钟之内打开本邮件中的链接并完成确认✅'),
          sender=current_app.config['ADMINS'][0],
          recipients=[user.email],
          text_body=render_template('email/registration.txt',
                                    user=user, link=link),
          html_body=render_template('email/registration.html',
                                    user=user, link=link),
          pic_attachments = pic_attachments,
          bcc=["admin@bgben.net"]
          )    
    return True


def send_reset_email(user):
    token = user.get_reset()
    link = url_for('users.reset_token', token=token, _external=True)

    pic_attachments = [{
      'folder_path': 'bgben/static/images',
      'filename': 'BGben_logo1.png',
      'content_type': 'image/png',
      'disposition': 'inline',
      'content-ID': '<BgbenLogo>'
    }]
    send_email(_('[BGben] 得知您想重置密码🔑，请在30分钟之内采取行动💪'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, link=link),
               html_body=render_template('email/reset_password.html',
                                         user=user, link=link),
               pic_attachments = pic_attachments,
               bcc=["admin@bgben.net"]
               )    

