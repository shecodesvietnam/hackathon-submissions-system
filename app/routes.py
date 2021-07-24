from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, SubmissionForm, GradeForm
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
            return redirect(url_for('teams_round_1'))
        elif current_user.role.name == 'Judge':
            return redirect(url_for('teams_round_2'))

    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Sai tên đăng nhập hoặc mật khẩu.')
            return redirect(url_for('login'))
        if user.role.name == 'Hacker' and not user.has_confirm:
            flash('You haven\'t confirm your team\'s account yet.')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        if user.role.name == 'Mentor':
            return redirect(url_for('teams_round_1'))
        elif user.role.name == 'Judge':
            return redirect(url_for('teams_round_2'))
        return redirect(url_for('submit'))
    return render_template('login.html', form=form, title='Login | Shecodes Hackathon')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    if current_user.role.name != 'Hacker':
        return render_template('401.html'), 401

    project = Project.query.filter_by(id=current_user.id).first()
    form = SubmissionForm()

    if form.validate_on_submit():
        if not is_valid_url(form.slide.data) or not is_valid_url(form.github.data):
            flash('Đường dẫn không hợp lệ, xin hãy thử lại.')
            return redirect(url_for('submit'))
        project.slide = form.slide.data
        project.github = form.github.data
        if form.youtube.data != '':
            if is_valid_url(form.youtube.data):
                project.youtube = form.youtube.data
            else:
                flash('Đường dẫn không hợp lệ, xin hãy thử lại.')
                return redirect(url_for('submit'))
        db.session.commit()
        flash('Nộp bài thành công!')
        return redirect(url_for('submit'))
    elif request.method == 'GET':
        form.slide.data = project.slide
        form.github.data = project.github
        form.youtube.data = project.youtube

    return render_template('submit.html', form=form, title='Submission | Shecodes Hackathon')


@app.route('/teams/round1')
@login_required
def teams_round_1():
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

    graded_projects = []
    not_graded_projects = []

    for row in get_graded_projects:
        graded_projects.append(row)

    for row in get_not_graded_projects:
        not_graded_projects.append(row)

    return render_template('teams_round_1.html', title='Round 1 | Shecodes Hackathon', graded_projects=graded_projects, not_graded_projects=not_graded_projects)


@app.route('/teams/round2')
@login_required
def teams_round_2():
    if current_user.role.name != 'Judge':
        return render_template('401.html'), 401

    top5_round1 = db.session.execute(f"""
    select project.id, project.name, project.slide, project.github, project.youtube, graderound2.total
    from graderound2
        join project on graderound2.project_id = project.id
        join users on graderound2.judge_id = users.id
    where graderound2.judge_id = {current_user.id};
    """)

    projects = []

    for row in top5_round1:
        projects.append(row)

    return render_template('teams_round_2.html', title='Round 2 | Shecodes Hackathon', projects=projects)


@app.route('/teams/round1/<project_name>/grading', methods=['GET', 'POST'])
@login_required
def grading_round_1(project_name):
    if current_user.role.name != 'Mentor':
        return render_template('401.html'), 401

    form = GradeForm()
    project = Project.query.filter_by(name=project_name).first()

    if request.method == 'POST':
        total = int(form.creative.data) + int(form.accessible.data) +int(form.demo.data) + int(form.techOption1.data) + int(form.techOption2.data) + int(form.techOption3.data) + int(form.pitching.data)
        if GradeRound1.query.filter_by(project_id=project.id).first():
            g = GradeRound1.query.filter_by(project_id=project.id).first()
            g.total = total
            db.session.add(g)
            db.session.commit()
        else:
            g = GradeRound1(mentor_id=current_user.id, project_id=project.id, total=total)
            db.session.add(g)
            db.session.commit()
        flash('Chấm điểm thành công!')
        return redirect(url_for('teams_round_1'))

    return render_template('grading_round_1.html', title='Grading Round 1 | Shecodes Hackathon', form=form, project=project)


@app.route('/teams/round2/<project_name>/grading', methods=['GET', 'POST'])
@login_required
def grading_round_2(project_name):
    print(current_user.role.name)
    if current_user.role.name != 'Judge':
        return render_template('401.html'), 401

    form = GradeForm()
    project = Project.query.filter_by(name=project_name).first()

    if request.method == 'POST':
        total = int(form.creative.data) + int(form.accessible.data) +int(form.demo.data) + int(form.techOption1.data) + int(form.techOption2.data) + int(form.techOption3.data) + int(form.pitching.data)
        g = GradeRound2.query.filter_by(project_id=project.id).first()
        g.total = total
        db.session.add(g)
        db.session.commit()
        flash('Chấm điểm thành công!')
        return redirect(url_for('teams_round_2'))

    return render_template('grading_round_2.html', title='Grading Round 2 | Shecodes Hackathon', form=form, project=project)


@app.route('/verify_reply/<token>', methods=['GET', 'POST'])
def verify_reply(token):
    user = User.verify_generated_token(token)
    if not user:
        return jsonify('Verify account failed'), 400
    user.has_confirm = True
    db.session.add(user)
    db.session.commit()
    return render_template('email/verify_reply_success.html')


@app.route('/test')
def test():
    user = User(name='The Impossible', username='the-impossible')
    password = '#fs"15%@dXv'
    return render_template('test.html', user=user, password=password)