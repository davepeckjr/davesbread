import os
from flask import *
#from flask.ext.login import LoginManager, current_user
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.ext.user import UserManager, SQLAlchemyAdapter, current_user
from flask.ext.mail import Mail
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD

davesbread = Flask(__name__)
davesbread.config.from_object('config')
db = SQLAlchemy(davesbread)

mail = Mail(davesbread)

from .models import User
db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, davesbread)

if not davesbread.debug and os.environ.get('HEROKU') is None:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/davesbread.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    davesbread.logger.addHandler(file_handler)
    davesbread.logger.setLevel(logging.INFO)
    davesbread.logger.info('davesbread startup')

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    davesbread.logger.addHandler(stream_handler)
    davesbread.logger.setLevel(logging.INFO)
    davesbread.logger.info('davesbread startup')

#lm = LoginManager()
#lm.init_app(davesbread)
#lm.login_view = 'login'
#@lm.user_loader
#def load_user(id):
#    return User.query.get(int(id))

from .models import User, MenuItems, Orders, OrderItems, Role, UserRole
class DavesBreadModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('user.login', next=request.url))

    column_exclude_list = ['password', 'registered_on', 'price', 'image_path',
                           'confirmed_at', 'email_confirmed', 'phone_num', 
                           'reset_password_token']

admin = Admin(davesbread, name="Dave's Bread", template_mode='bootstrap3')

admin.add_view(DavesBreadModelView(MenuItems, db.session))
admin.add_view(DavesBreadModelView(User, db.session))
admin.add_view(DavesBreadModelView(Role, db.session))
admin.add_view(DavesBreadModelView(Orders, db.session))
admin.add_view(DavesBreadModelView(OrderItems, db.session))

from davesbread import customer_views, manager_views, order_logic, models