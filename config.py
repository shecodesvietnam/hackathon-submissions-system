import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or 'Tallie1234'
    BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME") or 'admin'
    BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD") or '123456'
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    ADMINS = ['no-reply@shecodes-hackathon.com']

    # ? For sqlite
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # ? For postgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@localhost/HackathonSubmission'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TEAMS_PER_PAGE = 5
