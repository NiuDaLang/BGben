from flask import render_template, current_app, url_for
from flask_babel import _
from bgben.email import send_email


def send_message_email(recipient, sender, content):
    link = url_for('main.messages', username=recipient.username, tab='in', _external=True)

    pic_attachments = [{
      'folder_path': 'bgben/static/images',
      'filename': 'BGben_logo1.png',
      'content_type': 'image/png',
      'disposition': 'inline',
      'content-ID': '<BgbenLogo>'
    }, {
      'folder_path': 'bgben/static/profile_pics',
      'filename': sender.image_file,
      'content_type': 'image/png',
      'disposition': 'inline',
      'content-ID': '<AuthorPic>'
    }]

    send_email(_('[BGben]用户%(sender)s 刚刚向您发送了一条信息！', sender=sender.username),
               sender=current_app.config['ADMINS'][0],
               recipients=[recipient.email],
               text_body=render_template('email/send_message.txt',
                                         recipient_username=recipient.username, sender_username=sender.username, link=link, content=content),
               html_body=render_template('email/send_message.html',
                                         recipient_username=recipient.username, sender_username=sender.username, link=link, content=content),
               pic_attachments = pic_attachments,
               bcc=["admin@bgben.net"]
               )


def send_contact_confirm_email(user, user_email, category, content):
  pic_attachments = [{
    'folder_path': 'bgben/static/images',
    'filename': 'BGben_logo1.png',
    'content_type': 'image/png',
    'disposition': 'inline',
    'content-ID': '<BgbenLogo>'
  }]

  send_email(_('[BGben] 收到了您发出的信号✉️，会尽快回复的🫡'),
              sender=current_app.config['ADMINS'][0],
              recipients=[user_email],
              text_body=render_template('email/contact_receipt.txt',
                                        user=user, category=category, content=content),
              html_body=render_template('email/contact_receipt.html',
                                        user=user, category=category, content=content),
              pic_attachments = pic_attachments,
              bcc=["admin@bgben.net"]
              )
    

def send_newsletter_subscription_email(subscriber):
    token = subscriber.get_registered()
    link = url_for('main.nl_sub_confirm', token=token, _external=True)

    pic_attachments = [{
        'folder_path': 'bgben/static/images',
        'filename': 'BGben_logo1.png',
        'content_type': 'image/png',
        'disposition': 'inline',
        'content-ID': '<BgbenLogo>'
    }]

    send_email(_('欢迎申请[BGben]通讯，请在30分钟之内打开本邮件中的链接并完成确认✅'),
          sender=current_app.config['ADMINS'][0],
          recipients=[subscriber.email],
          text_body=render_template('email/newsletter_sub_confirm.txt', link=link),
          html_body=render_template('email/newsletter_sub_confirm.html', link=link),
          pic_attachments = pic_attachments,
          bcc=["admin@bgben.net"]
          )    

    return True
