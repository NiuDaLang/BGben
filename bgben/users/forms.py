from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from bgben import db
from bgben.models import User
from flask_babel import _, lazy_gettext as _l
import sqlalchemy as sa


class TestPassForm (FlaskForm):
    test = StringField("test")
    submit_field = SubmitField(_l("欢 迎 注 册 👏"))

class RegistrationForm (FlaskForm):
    username = StringField(_l("BGben用户名"), render_kw={"placeholder": _l('BGben用户名(昵称 2~10字)')},
                           validators=[DataRequired(), Length(min=2, max=10, message=_l("字数规定：2～10字"))])
    email = StringField(_l("邮箱"), render_kw={"placeholder": _l('邮箱')},
                        validators=[DataRequired(), Email(message=_l("邮箱地址格式不正确，请确认再输入一遍"))])
    password = PasswordField(_l("密码"), render_kw={"placeholder": _l('密码(6~30字)')},
                             validators=[DataRequired(),
                                        Regexp('(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[-_#\$%&\*])[0-9a-zA-Z_\-#\$%&\*]{8,30}', message=_l("6～30字，含大、小字符、数字各至少1字，特殊字符—_#$%&*至少1字符")),
                                        Length(min=6, max=30, message=_l("总共字数6～30个"))])
    confirm_password = PasswordField(_l("密码确认"), render_kw={"placeholder": _l('密码确认')},
                             validators=[DataRequired(),
                                        EqualTo('password', message=_l("请输入相同的密码"))])
    agree = BooleanField(_l("同意"), validators=[DataRequired()])
    submit_field = SubmitField(_l("注 册"))

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError(_('此用户名已被使用，请选用其他名字！'))
    
    def validate_email(self, email):
        email = db.session.scalar(sa.select(User).where(User.email == email.data))
        if email is not None:
            raise ValidationError(_('此邮箱已被使用，请选用其他邮箱！'))

class LoginForm (FlaskForm):
    email = StringField(_l("邮箱"), render_kw={"placeholder": _l("邮箱")},
                        validators=[DataRequired(), Email(message=_l("邮箱地址格式不正确，请确认再输入一遍"))])
    password = PasswordField(_l("密码"), render_kw={"placeholder": _l("密码")},
                             validators=[DataRequired()])
    remember = BooleanField(_l("记住我"))
    submit_field = SubmitField(_l("登 陆"))
  
class UpdateAccountForm(FlaskForm):
    username = StringField(_l("BGben用户名"), 
                           validators=[DataRequired(), Length(min=2, max=10, message=_l("字数规定：2～10字"))])
    email = StringField(_l("邮箱"),
                        validators=[DataRequired(), Email(message=_l("邮箱地址格式不正确，请确认再输入一遍"))])
    picture = FileField(_l('头像'), validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    zodiac_sign = RadioField(_l('星座'), choices=[
        ('aries', _l('白羊座')),
        ('taurus', _l('金牛座')),
        ('gemini', _('双子座')),
        ('cancer', _l('巨蟹座')),
        ('leo', _l('狮子座')),
        ('virgo', _l('处女座')),
        ('libra', _l('天秤座')),
        ('scorpio', _l('天蝎座')),
        ('sagittarius', _l('射手座')),
        ('capricorn', _l('摩羯座')),
        ('aquarius', _l('水瓶座')),
        ('pisce', _l('双鱼座')),
        ('unknown', _l('未知'))],
    )
    about_me = TextAreaField(_l('关于我'), validators=[Length(min=0, max=120)], render_kw={"placeholder": _l('120字以内')})
    submit_field = SubmitField(_l("更 新"))

    def validate_username(self, username):
        if username.data != current_user.username:
            user = db.session.scalar(sa.select(User).where(User.username == username.data))
            if user is not None:
                raise ValidationError(_('此用户名已被使用，请选用其他名字！'))
    
    def validate_email(self, email):
        if email.data != current_user.email:
            email = db.session.scalar(sa.select(User).where(User.email == email.data))
            if email is not None:
                raise ValidationError(_('此邮箱已被使用，请选用其他邮箱！'))


class RequestResetForm(FlaskForm):
    email = StringField(_l("邮箱"),
                        validators=[DataRequired(), Email(message=_l("邮箱地址格式不正确，请确认再输入一遍"))])
    submit_field = SubmitField(_l("我要重置密码"))

    def validate_email(self, email):
        email = db.session.scalar(sa.select(User).where(User.email == email.data).where(User.active == True))
        if email is None:
            raise ValidationError(_('此邮箱用户尚未注册！请注册'))
        elif email and not email.active:
            raise ValidationError(_('此邮箱用户已停用！请重新注册'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l("密码"), 
                             validators=[DataRequired(),
                                        Regexp('(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[-_#\$%&\*])[0-9a-zA-Z_\-#\$%&\*]{8,30}', message=_l("总共字数6～30个，含大、小字符、数字各至少1字，特殊字符 —_#$%&*至少1字符")),
                                        Length(min=6, max=30, message=_l("总共字数6～30个"))], render_kw={"placeholder": _l('新的密码')})
    confirm_password = PasswordField(_l("密码确认"), 
                                     validators=[DataRequired(),
                                                 EqualTo('password', message=_l("请输入相同的密码"))], render_kw={"placeholder": _l('请在输入一遍新的密码')})
    submit_field = SubmitField(_l("重置密码"))


class EmptyForm(FlaskForm):
    submit = SubmitField(_l("关注TA"))


class UnfollowForm(FlaskForm):
    submit = SubmitField(_l("取消关注"))