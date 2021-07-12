from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import URLType
from flask_login import UserMixin
from app import app, db, login
from app.utils import generate_username

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(100))
    proj_name = db.Column(db.String(100))
    slide = db.Column(URLType)
    github = db.Column(URLType)
    youtube = db.Column(URLType)
    is_judge = db.Column(db.Boolean)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_username(self):
        self.username = generate_username(self.name)

    def __repr__(self) -> str:
        return f'<Username: {self.username}, Is judge: {self.is_judge}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))