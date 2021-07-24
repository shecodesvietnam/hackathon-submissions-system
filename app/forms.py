from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url, Length
from wtforms.widgets.html5 import NumberInput


class LoginForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    submit = SubmitField('Đăng nhập')


class SubmissionForm(FlaskForm):
    slide = URLField('Slide link:', validators=[DataRequired(), url()])
    github = URLField('Github Link:', validators=[DataRequired(), url()])
    youtube = URLField('Youtube link (không bắt buộc):')
    submit = SubmitField('Nộp bài')


class GradeForm(FlaskForm):
    creative = RadioField('Creative', choices=[
        (15, 'Ý tưởng này hoàn toàn độc đáo, chưa tìm thấy tại thị trường Việt Nam. (15đ)'),
        (10, 'Ý tưởng này đã tồn tại, tuy nhiên được phát triển và hoàn thiện theo một hướng mới để giải quyết vấn đề một cách hiệu quả hơn. (10đ)'),
        (0, 'Ý tưởng này chưa có gì độc đáo và khó có thể cạnh tranh với các ý tưởng tương tự trong thị trường. (0đ)')
    ], validators=[DataRequired()])
    accessible = RadioField('Accessible', choices=[
        (30, 'Ý tưởng này giải quyết một vấn đề ý nghĩa trong xã hội, mang đến tác động tích cực cho một nhóm đối tượng cụ thể (là nhóm người yếu thế như đề bài đã ra) về mặt kinh tế/môi trường/cộng đồng, và có thể thực hiện được. (30đ)'), 
        (20, 'Ý tưởng này giải quyết một vấn đề ý nghĩa trong xã hội, mang đến tác động tích cực cho một nhóm đối tượng cụ thể về mặt kinh tế/môi trường/cộng đồng, tuy nhiên không thể thực hiện được vì Công nghệ thông tin chưa cho phép. (20đ)'),
        (10, 'Ý tưởng này có thể thực hiện được, tuy nhiên không thực sự giải quyết một vấn đề có ý nghĩa trong xã hội, và không mang đến tác động tích cực cho một nhóm đối tượng cụ thể nào. (10đ)'),
        (0, 'Ý tưởng này phi thực tế và không mang lại tác động tích cực cho một nhóm đối tượng cụ thể nào. (0đ)')
    ], validators=[DataRequired()])
    demo = RadioField('Demo', choices=[
        (15, 'Chạy đúng như mô tả hoặc chỉ có vài lỗi nhỏ. (15đ)'),
        (10, 'Có sản phẩm nhưng chưa đầy đủ như mô tả hoặc có lỗi nghiêm trọng (không thể chạy, không thực hiện được chức năng chính). (10đ)'),
        (0, 'Không có demo. (0đ)')
    ], validators=[DataRequired()])
    techOption1 = IntegerField('Công nghệ mới và độc đáo (tối đa 20đ)', validators=[DataRequired(), Length(min=0, max=20)], widget=NumberInput(min=0, max=20))
    techOption2 = IntegerField('Thể hiện được ý tưởng thông qua bản thiết kế (tối đa 10đ)', validators=[DataRequired(), Length(min=0, max=10)], widget=NumberInput(min=0, max=10))
    techOption3 = IntegerField('Mức độ thiết kế trải nghiệm người dùng (tối đa 10đ)', validators=[DataRequired(), Length(min=0, max=10)], widget=NumberInput(min=0, max=10))
    pitching = IntegerField('', validators=[DataRequired(), Length(min=0, max=10)], widget=NumberInput(min=0, max=10))
    submit = SubmitField('Kết thúc chấm điểm')