from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url, NumberRange
from wtforms.widgets.html5 import NumberInput


class LoginForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    submit = SubmitField('Đăng nhập')


class SubmissionForm(FlaskForm):
    slide = URLField('Link slides thuyết trình sản phẩm:', validators=[DataRequired(), url()])
    github = URLField('Link github repository:', validators=[DataRequired(), url()])
    youtube = URLField('Link video demo:', validators=[DataRequired(), url()])
    others = URLField('Link docs mô tả feature sản phẩm:', validators=[DataRequired(), url()])
    submit = SubmitField('Nộp bài')


class GradeFormMentor(FlaskForm):
    creative = IntegerField(validators=[NumberRange(min=0, max=15)], widget=NumberInput(min=0, max=15))
    accessible = IntegerField(validators=[NumberRange(min=0, max=30)], widget=NumberInput(min=0, max=30))
    demo = IntegerField(validators=[NumberRange(min=0, max=15)], widget=NumberInput(min=0, max=15))
    techOption1 = IntegerField('Công nghệ mới và độc đáo (tối đa 20đ)', validators=[NumberRange(min=0, max=20)], widget=NumberInput(min=0, max=20))
    techOption2 = IntegerField('Thể hiện được ý tưởng thông qua bản thiết kế (tối đa 10đ)', validators=[NumberRange(min=0, max=10)], widget=NumberInput(min=0, max=10))
    techOption3 = IntegerField('Mức độ thiết kế trải nghiệm người dùng (tối đa 10đ)', validators=[NumberRange(min=0, max=10)], widget=NumberInput(min=0, max=10))
    submit = SubmitField('Kết thúc chấm điểm')


class GradeFormJudge(FlaskForm):
    creative = IntegerField(validators=[NumberRange(min=0, max=15)], widget=NumberInput(min=0, max=15))
    accessible = IntegerField(validators=[NumberRange(min=0, max=30)], widget=NumberInput(min=0, max=30))
    demo = IntegerField(validators=[NumberRange(min=0, max=15)], widget=NumberInput(min=0, max=15))
    techOption1 = IntegerField('Công nghệ mới và độc đáo (tối đa 20đ)', validators=[NumberRange(min=0, max=20)], widget=NumberInput(min=0, max=20))
    techOption2 = IntegerField('Thể hiện được ý tưởng thông qua bản thiết kế (tối đa 10đ)', validators=[NumberRange(min=0, max=10)], widget=NumberInput(min=0, max=10))
    techOption3 = IntegerField('Mức độ thiết kế trải nghiệm người dùng (tối đa 10đ)', validators=[NumberRange(min=0, max=10)], widget=NumberInput(min=0, max=10))
    pitching = IntegerField(validators=[NumberRange(min=0, max=10)], widget=NumberInput(min=0, max=10))
    submit = SubmitField('Kết thúc chấm điểm')