from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, SubmissionForm
from app.models import User
from app.utils import is_valid_url


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_judge:
            return redirect(url_for('list_teams'))
        else:
            return redirect(url_for('submit'))

    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        if user.is_judge:
            return redirect(url_for('list_teams'))
        return redirect(url_for('submit'))
    return render_template('login.html', form=form, title='Login | Shecodes Hackathon')


@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    if current_user.is_judge:
        return render_template('401.html'), 401

    form = SubmissionForm()

    if form.validate_on_submit():
        if not is_valid_url(form.slide.data) or not is_valid_url(form.github.data):
            flash('Invalid Url, please check again.')
            return redirect(url_for('submit'))
        current_user.slide = form.slide.data
        current_user.github = form.github.data
        if form.youtube.data != '':
            if is_valid_url(form.youtube.data):
                current_user.youtube = form.youtube.data
            else:
                flash('Invalid Url, please check again.')
                return redirect(url_for('submit'))
        db.session.commit()
        flash('Submitted successfully')
        return redirect(url_for('submit'))
    elif request.method == 'GET':
        form.slide.data = current_user.slide
        form.github.data = current_user.github
        form.youtube.data = current_user.youtube

    return render_template('submit.html', form=form, title='Submission | Shecodes Hackathon', participant=current_user)

@app.route('/teams')
@login_required
def list_teams():
    if not current_user.is_judge:
        return render_template('401.html'), 401

    page = request.args.get('page', 1, type=int)
    teams = User.query.filter_by(is_judge=False).paginate(
        page, app.config['TEAMS_PER_PAGE'], False
    )
    next_url = url_for('list_teams', page=teams.next_num) if teams.has_next else None
    prev_url = url_for('list_teams', page=teams.prev_num) if teams.has_prev else None

    return render_template('list_teams.html', title='Teams | Shecodes Hackathon', teams=teams.items, next_url=next_url, prev_url=prev_url)