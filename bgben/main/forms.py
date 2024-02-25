from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask_babel import _, lazy_gettext as _l
from bgben import db
from bgben.models import Newsletter
import sqlalchemy as sa


class SearchForm(FlaskForm):
  q = StringField(_l(' ✏️ 搜索'), validators=[DataRequired()])

  def __init__(self, *args, **kwargs):
    if 'formdata' not in kwargs:
      kwargs['formdata'] = request.args
    if 'meta' not in kwargs:
      kwargs['meta'] = {'csrf': False}
    super(SearchForm, self).__init__(*args, **kwargs)


class MessageForm(FlaskForm):
  message = TextAreaField(_l('Message'), validators=[DataRequired(), Length(min=0, max=140)], render_kw=({"placeholder_": _l('140字以内')}))
  submit_field = SubmitField(_l('发 送'))


CONTACT_CATEGORIES = [('default', _l('请从以下选择')), ('consult', _l('咨询')), ('web', _l('网页·网站制作')), ('suggestion', _l('建议')), ('jv', _l('合作')), ('other', _l('其他'))]

class ContactForm(FlaskForm):
  name = StringField(_l("名字"), validators=[DataRequired(_l("请输入名字"))], render_kw={"placeholder": _l('姓名（或昵称）')})
  email = StringField(_l("邮箱"), render_kw={"placeholder": _l('邮箱')},
                      validators=[DataRequired(_l("请输入邮箱地址")), Email(message=_l("邮箱地址格式不正确，请确认再输入一遍"))])
  
  category = SelectField(_l("关于"), choices=CONTACT_CATEGORIES)

  content = TextAreaField(_l('内容'), validators=[DataRequired(_l("请输入联系内容")), Length(min=2, max=500)], render_kw=({"placeholder_": _l('500字以内')}))
  submit_field = SubmitField(_l("发 送"))


class DeleteForm(FlaskForm):
  submit = SubmitField(_l("删除"))


class NewsletterForm(FlaskForm):
  email = StringField(_l("邮箱"), render_kw={"placeholder": _l('请输入邮箱地址')},
                    validators=[DataRequired(message=_l("请输入邮箱地址！")), Length(min=6, max=120, message=_l("邮箱地址字数最少6个字，最多120字。")), Email(message=_l("邮箱地址格式不正确，请确认再输入一遍"))])
  submit_field = SubmitField(_l("订 阅"))

  def validate_email(self, email):
    email = db.session.scalar(sa.select(Newsletter).where(Newsletter.email == email.data))
    if email is not None:
        raise ValidationError(_l('此邮箱已被使用，请选用其他邮箱！'))


