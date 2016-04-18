import os

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = '+{Tom@to8asil}+'

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#Flask-User Settions
USER_ENABLE_USERNAME = False
USER_ENABLE_CHANGE_USERNAME = False
USER_PASSWORD_HASH = 'bcrypt'
USER_APP_NAME = "Dave's Bread"

#Mail Server Settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'davepeckjr@gmail.com'
MAIL_PASSWORD = 'K1rkl4nd#'
MAIL_DEFAULT_SENDER = ["Dave's Bread",'no-reply@davesbread.com']

#Admin List
ADMINS = ['davepeckjr@gmail.com']