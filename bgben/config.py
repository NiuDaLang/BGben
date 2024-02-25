import os
from dotenv import load_dotenv
from flask import url_for

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY')
  # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
  SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                            'sqlite:///' + os.path.join(basedir, 'site.db')
  # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db_test' // for unittest

  FLASK_DEBUG=os.environ.get('FLASK_DEBUG')

  MAIL_SERVER = os.environ.get('MAIL_SERVER')
  MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
  MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  MAIL_DEFAULT_SENDER : os.environ.get('MAIL_DEFAULT_SENDER')

  SQLALCHEMY_TRACK_MODIFICATIONS = False
  ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
  LANGUAGES = ['zh', 'ja', 'en']
  REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'

  ADMINS = os.environ.get('ADMINS').strip('[]').split(',')
  

  CKEDITOR_FILE_UPLOADER = 'posts.upload'
  CKEDITOR_ENABLE_CSRF = True
