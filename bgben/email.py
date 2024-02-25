from threading import Thread
from flask import current_app
from flask_mail import Message
from bgben import mail


def send_async_email(app, msg):
  with app.app_context():
    mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body, cc=None, bcc=None, pic_attachments=None, attachments=None, sync=False):
  msg = Message(subject, sender=sender, recipients=recipients)
  msg.body = text_body
  msg.html = html_body
  if cc:
    msg.cc = cc
  if bcc:
    msg.bcc = bcc
  if pic_attachments:
    for pic_attachment in pic_attachments:
      with open("/".join([pic_attachment['folder_path'], pic_attachment['filename']]), 'rb') as fp:
        data= fp.read()
      msg.attach(
        filename=pic_attachment['filename'],
        content_type=pic_attachment['content_type'],
        data=data,
        disposition=pic_attachment['disposition'],
        headers=[['Content-ID', pic_attachment['content-ID']]])
  if attachments:
    for attachment in attachments:
      msg.attach(*attachment)
  if sync:
    mail.send(msg)
  else:
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()
