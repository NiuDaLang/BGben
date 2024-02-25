from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, FieldList
from wtforms.validators import DataRequired, Length
from flask_babel import lazy_gettext as _l


class CreatePostForm(FlaskForm):
    title = StringField(_l("标题"), validators=[DataRequired(_l("请输入标题")), Length(min=1, max=30, message=_l("字数规定：1～30字"))], render_kw={"placeholder": _l('30字以内')})
    subtitle = StringField(_l("副标题"), validators=[DataRequired(_l("请输入副标题")), Length(min=1, max=100, message=_l("字数规定：1～100字"))], render_kw={"placeholder": _l('100字以内')})
    main_picture = FileField(_l('主题图像'), validators=[FileAllowed(['jpg', 'jpeg', 'png'], _l("可上传的图像文件格式：jpg、jpeg、png"))])
    body = CKEditorField(_l('内容'), validators=[DataRequired(_l("请输入内容")), Length(min=1, max=50000, message=_l("字数规定：1～3000字"))], render_kw={"placeholder": _l('3000字以内')})
    tags = FieldList(StringField('#', validators=[Length(min=0, max=50)]), min_entries=1, max_entries=6)
    submit_field = SubmitField(_l("投 稿"))


class CommentForm(FlaskForm):
  comment = StringField(_l("评论"), validators=[DataRequired(_l("请输入评论内容")), \
                        Length(min=1, max=250, message=_l("字数规定：2～200字"))], render_kw={"placeholder": _l('200字以内')})
  submit_field = SubmitField(_l("提 交"))


