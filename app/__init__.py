from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors, email, forms, utils

from app.administrator import init_admin
init_admin(app)