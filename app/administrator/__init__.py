from flask_admin.base import AdminIndexView, expose
from werkzeug.exceptions import HTTPException
from flask import Response, redirect
from flask_basicauth import BasicAuth
from flask_admin import Admin
from flask_admin.contrib import sqla
from sqlalchemy import func
from app import db
from app.models import User, Role, Project, GradeRound1, GradeRound2
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
        form_excluded_columns = ('username', 'password_hash', 'project', 'grade_round_1', 'grade_round_2', 'has_confirm')

        def on_model_change(self, form, model, is_created):
            if is_created:
                password = generate_random_password()
                model.set_password(password)
                model.set_username()
                if model.role.name != 'Hacker':
                    model.has_confirm = True
                send_team_account_email(model, password)
            return super().on_model_change(form, model, is_created)

    
    class RoleModelView(ModelView):
        column_exclude_list = ('team')
        form_excluded_columns = ('team_id')

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)

    
    class ProjectModelView(ModelView):
        form_excluded_columns = ('grade_round_1', 'grade_round_2', 'timestamp')
        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
        
    class GradeRound1ModelView(ModelView):
        can_create = False
        can_edit = False
        can_delete = False
        column_list = ('mentor_id', 'project_id', 'total')

        # def on_model_change(self, form, model, is_created):
        #     return super().on_model_change(form, model, is_created)

    class GradeRound2ModelView(ModelView):
        can_create = False
        can_edit = False
        can_delete = False
        column_list = ('judge_id', 'project_id', 'total')

        # def on_model_change(self, form, model, is_created):
        #     return super().on_model_change(form, model, is_created)

    class HomeView(AdminIndexView):
        @expose('/')
        def index(self):
            command = f"""
            select project.id, project.name, project.slide, project.github, project.youtube, sum(graderound2.total) as total
            from graderound2
                join project on graderound2.project_id = project.id
                join users on graderound2.judge_id = users.id
            group by project.id
            order by total desc
            """
            projects = db.session.execute(command)
            return self.render('admin/home.html', projects=projects)

    admin = Admin(app, index_view=HomeView(), template_mode='bootstrap3')
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(RoleModelView(Role, db.session))
    admin.add_view(ProjectModelView(Project, db.session))
    admin.add_view(GradeRound1ModelView(GradeRound1, db.session))
    admin.add_view(GradeRound2ModelView(GradeRound2, db.session))
    