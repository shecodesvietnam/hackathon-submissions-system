from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class SubmissionForm(FlaskForm):
    slide = URLField('Slide Link', validators=[DataRequired(), url()])
    github = URLField('GitHub Link', validators=[DataRequired(), url()])
    youtube = URLField('Youtube Link (optional)')
    submit = SubmitField('Submit')