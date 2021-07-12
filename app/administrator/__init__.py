from werkzeug.exceptions import HTTPException
from flask import Response, redirect
from flask_basicauth import BasicAuth
from flask_admin import Admin
from flask_admin.contrib import sqla
from app import db
from app.models import User
from app.utils import generate_random_password
from app.email import send_team_account_email

def init_admin(app):
    basic_auth = BasicAuth(app)

    class AuthException(HTTPException):
        def __init__(self, message):
            super().__init__(message, Response(
                message, 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            ))

    
    class ModelView(sqla.ModelView):
        def is_accessible(self):
            if not basic_auth.authenticate():
                raise AuthException('Not authenticated. Refresh the page.')
            else:
                return True

        def inaccessible_callback(self, name, **kwargs):
            return redirect(basic_auth.challenge())

    
    class UserModelView(ModelView):
        column_exclude_list = ('password_hash')
        form_excluded_columns = ('username', 'password_hash', 'slide', 'github', 'youtube')

        def on_model_change(self, form, model, is_created):
            if is_created:
                password = generate_random_password()
                model.set_password(password)
                model.set_username()
                # send_team_account_email(model, password)
            return super().on_model_change(form, model, is_created)

    admin = Admin(app)
    admin.add_view(UserModelView(User, db.session))