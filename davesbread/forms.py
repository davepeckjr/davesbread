from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, SubmitField,\
                    SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email
from davesbread.models import User, MenuItems

class LoginForm(Form):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField("Sign In")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    
    def validate(self):
        if not Form.validate(self):
            return False
        
        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid e-mail or password")
            return False

class SignupForm(Form):
    firstname = StringField("First name", validators=[DataRequired()])
    lastname = StringField("Last name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Create account")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        
    def validate(self):
        if not Form.validate(self):
            return False
        
        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
            self.email.errors.append("Email already in use")
            return False
        else:
            return True

class OrderForm(Form):
    side = SelectField('Side', coerce=int, 
                        choices=[(s.id, s.name) for s in\
                        MenuItems.query.filter_by(category='side').all()])
                        
    quantity = IntegerField(default=1)
    submit = SubmitField("Add to Order")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

class EditOrderForm(Form):
    side = SelectField('Side', coerce=int,
                        choices=[(s.id, s.name) for s in\
                        MenuItems.query.filter_by(category='side').all()])
                       
    quantity = IntegerField(default=1)
    submit = SubmitField("Update Order")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
