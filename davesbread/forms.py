from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, SubmitField,\
                    SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from wtforms.ext.dateutil.fields import DateTimeField
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

class UpdateProfileForm(Form):
    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])
    phone_num = IntegerField("Phone Number", validators=[DataRequired()])
    submit = SubmitField("Save")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

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

class FinalForm(Form):
#This isn't even my final form.....
    pick_up_time = DateTimeField('Pickup Time', display_format='%d-%m-%Y %H:%M')
    special_instructions = StringField("Special Instructions")
    submit = SubmitField("Submit")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    
    def validate(self):
        if not Form.validate(self):
            return False

class ContactCustomerForm(Form):
    body = TextAreaField(validators=[DataRequired()])
    submit = SubmitField("Send")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    
    def validate(self):
        if not Form.validate(self):
            return False