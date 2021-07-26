import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import URLType
from flask_login import UserMixin
from app import app, db, login
from app.utils import generate_username

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    has_confirm = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(100))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='team')
    grade_round_1 = db.relationship(
        'Project',
        secondary='graderound1',
        backref='grade_round_1',
        lazy='dynamic'
    )
    grade_round_2 = db.relationship(
        'Project',
        secondary='graderound2',
        backref='grade_round_2',
        lazy='dynamic'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_username(self):
        self.username = generate_username(self.name)

    def get_generated_token(self):
        return jwt.encode({'generated_token': self.password_hash}, app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_generated_token(token):
        try:
            password_hash = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['generated_token']
        except:
            return
        return User.query.filter_by(password_hash=password_hash).first()

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'<Username: {self.username}, Role: {self.role.name}>'


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self) -> str:
        return f'<Role: {self.name}>'

    def __str__(self) -> str:
        return f'{self.name}'


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100), index=True, unique=True)
    slide = db.Column(URLType, nullable=True)
    github = db.Column(URLType, nullable=True)
    youtube = db.Column(URLType, nullable=True)
    timestamp = db.Column(db.String(100), index=True)
    team = db.relationship('User', backref='project')

    def __repr__(self) -> str:
        return f'<Project: {self.name}>'

    def __str__(self) -> str:
        return f'{self.name}'


class GradeRound1(db.Model):
    __tablename__ = 'graderound1'
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    total = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f'<Grade round 1, mentor_id: {self.mentor_id}, project_id: {self.project_id}>'


class GradeRound2(db.Model):
    __tablename__ = 'graderound2'
    judge_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    total = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f'<Grade round 2, judge_id: {self.judge_id}, project_id: {self.project_id}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))