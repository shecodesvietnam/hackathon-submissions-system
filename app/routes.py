from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, SubmissionForm
from app.models import User, Role, Project, GradeRound1, GradeRound2
from app.utils import is_valid_url


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role.name == 'Hacker':
            return redirect(url_for('submit'))
        elif current_user.role.name == 'Mentor':
            return redirect(url_for('grading_round_1'))
        elif current_user.role.name == 'Judge':
            return redirect(url_for('grading_round_2'))

    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        if user.role.name == 'Mentor':
            return redirect(url_for('grading_round_1'))
        elif user.role.name == 'Judge':
            return redirect(url_for('grading_round_2'))
        return redirect(url_for('submit'))
    return render_template('login.html', form=form, title='Login | Shecodes Hackathon')


@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    if current_user.role.name != 'Hacker':
        return render_template('401.html'), 401

    project = Project.query.filter_by(id=current_user.id).first()
    form = SubmissionForm()

    if form.validate_on_submit():
        if not is_valid_url(form.slide.data) or not is_valid_url(form.github.data):
            flash('Invalid Url, please check again.')
            return redirect(url_for('submit'))
        project.slide = form.slide.data
        project.github = form.github.data
        if form.youtube.data != '':
            if is_valid_url(form.youtube.data):
                project.youtube = form.youtube.data
            else:
                flash('Invalid Url, please check again.')
                return redirect(url_for('submit'))
        db.session.commit()
        flash('Submitted successfully')
        return redirect(url_for('submit'))
    elif request.method == 'GET':
        form.slide.data = project.slide
        form.github.data = project.github
        form.youtube.data = project.youtube

    return render_template('submit.html', form=form, title='Submission | Shecodes Hackathon')


@app.route('/grading/round1')
@login_required
def grading_round_1():
    if current_user.role.name != 'Mentor':
        return render_template('401.html'), 401

    get_graded_projects = db.session.execute(f"""
    select project.id as project_id, project.name, project.slide, project.github, project.youtube, graderound1.total
    from project
    join graderound1 on graderound1.project_id = project.id
    join users on graderound1.mentor_id = users.id
    where mentor_id = {current_user.id};
    """)

    get_not_graded_projects = db.session.execute(f"""
    select project.id , project.name, project.slide, project.github, project.youtube
    from project
    where project.id not in (
        select project.id from project
            join graderound1 on graderound1.project_id = project.id
            join users on graderound1.mentor_id = users.id
        where mentor_id = {current_user.id}
    ) 
    """)

    graded_teams = []
    not_graded_teams = []

    for row in get_graded_projects:
        graded_teams.append(row)

    for row in get_not_graded_projects:
        not_graded_teams.append(row)

    return render_template('grading_round_1.html', title='Round 1 | Shecodes Hackathon', graded_teams=graded_teams, not_graded_teams=not_graded_teams)


@app.route('/grading/round2')
@login_required
def grading_round_2():
    if current_user.role.name != 'Judge':
        return render_template('401.html'), 401

    get_round_2_projects = db.session.execute(f"""
    select project.id as project_id, project.name, project.slide, project.github, project.youtube, graderound2.total
    from project
    join graderound2 on graderound2.project_id = project.id
    join users on graderound2.judge_id = users.id
    where judge_id = {current_user.id};
    """)

    teams = []

    for row in get_round_2_projects:
        teams.append(row)

    return render_template('grading_round_2.html', title='Round 2 | Shecodes Hackathon', teams=teams)