from flask import render_template, Blueprint, request
from bgben import db
import re


errors = Blueprint('errors', __name__)

@errors.app_errorhandler(400)
def bad_request_error(error):
    return render_template('errors/400.html', re=re), 400


@errors.app_errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html', re=re), 403


@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html', re=re), 404


@errors.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html', re=re), 500


def return_previous():
  return request.referrer
