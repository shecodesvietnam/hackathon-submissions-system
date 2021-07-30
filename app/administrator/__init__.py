from flask_admin.base import AdminIndexView, BaseView, expose
from werkzeug.exceptions import HTTPException
from flask import Response, redirect, flash
from flask_basicauth import BasicAuth
from flask_admin import Admin
from flask_admin.contrib import sqla
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
        column_list = ('id', 'role', 'username', 'name', 'email', 'has_confirm')
        # column_exclude_list = ('password_hash')
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
        column_list = ('id', 'team', 'name', 'slide', 'github', 'youtube', 'others', 'timestamp')
        form_excluded_columns = ('grade_round_1', 'grade_round_2', 'timestamp')
        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)
        
    class GradeRound1ModelView(ModelView):
        # can_create = False
        # can_edit = False
        # can_delete = False
        column_list = ('mentor_id', 'project_id', 'total')
        form_columns = ('mentor_id', 'project_id')

        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)

    class GradeRound2ModelView(ModelView):
        list_template = "admin/list_view.html"
        # can_create = False
        # can_edit = False
        # can_delete = False
        column_list = ('judge_id', 'project_id', 'total')
        form_columns = ('judge_id', 'project_id')

        @expose('/get_round_2')
        def get_round_2(self):
            try:
                round2 = GradeRound2.query.all()
                if len(round2) == 0:
                    judges = db.session.query(User, Role).filter(Role.name=='Judge').join(User, User.role_id==Role.id).all()

                    top5_round1 = db.session.execute(f"""
                    select project.id as project_id, 
                        project.name, 
                        project.slide, 
                        project.github, 
                        project.youtube, 
                        sum(graderound1.total) as total
                    from project
                    join graderound1 on graderound1.project_id = project.id
                    join users on graderound1.mentor_id = users.id
                    group by project.id
                    order by total desc
                    limit 5;
                    """)

                    for team in top5_round1:
                        print('outer')
                        for judge in judges:
                            print('inner')
                            g = GradeRound2(judge_id=judge[0].id, project_id=team.project_id)
                            db.session.add(g)
                            db.session.commit()

                    flash('Top 5 teams has added to round 2!')
                else:
                    flash('Nothing changed, get top 5 only works when round 2 has no records.')
                return redirect('/admin/graderound2')
            except Exception as e:
                if not self.handle_view_exception(e):
                    raise

                flash("Failed to get top 5.")
                return redirect('/admin/graderound2')


        def on_model_change(self, form, model, is_created):
            return super().on_model_change(form, model, is_created)

    class HomeView(AdminIndexView):
        @expose('/')
        def index(self):
            projects = db.session.execute(f"""
            select project.id, project.name, project.slide, project.github, project.youtube, sum(graderound2.total) as total
            from graderound2
                join project on graderound2.project_id = project.id
                join users on graderound2.judge_id = users.id
            group by project.id
            order by total desc
            """)
            return self.render('admin/home.html', projects=projects)


    class MentorGradingProcessView(BaseView):
        @expose('/')
        def index(self):
            processes = db.session.execute(f"""
            SELECT users.id, users.name as mentor_name, COUNT(users.id) AS grading_process
            FROM users
                JOIN graderound1 ON graderound1.mentor_id = users.id
            GROUP BY users.id
            """)
            total_projects = len(Project.query.all())
            result = []
            for process in processes:
                result.append({
                    'id': process.id,
                    'mentor_name': process.mentor_name,
                    'grading_process': f'{process.grading_process}/{total_projects}'
                })
            return self.render('admin/mentor_grading_process.html', processes=result)

    admin = Admin(app, index_view=HomeView(), template_mode='bootstrap3')
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(RoleModelView(Role, db.session))
    admin.add_view(ProjectModelView(Project, db.session))
    admin.add_view(GradeRound1ModelView(GradeRound1, db.session))
    admin.add_view(MentorGradingProcessView(name='Mentor Grading Process', endpoint='mentorgradingprocess'))
    admin.add_view(GradeRound2ModelView(GradeRound2, db.session))
    