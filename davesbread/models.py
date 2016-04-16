from davesbread import db, davesbread
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.user import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, unique=False)
    last_name = db.Column(db.String(64), index=True, unique=False)
    is_enabled = db.Column(db.Boolean(), default=True)
    
    registered_on = db.Column(db.DateTime)
    
    email = db.Column(db.String(120), index=True, unique=True)
    email_confirmed = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    phone_num = db.Column(db.Integer(), index=True, unique=True)
    password = db.Column(db.String(54))
    reset_password_token = db.Column(db.String(100), default='')
    

    
    roles = db.relationship('Role', 
                            secondary='user_role',
                            backref='user', 
                            lazy='dynamic')
    
    orders = db.relationship('Orders', backref='user', lazy='dynamic')
    """
    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.password = password
        self.is_enabled = is_enabled
    
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
    """
    @property
    def is_authenticated(self):
        return True
        
    @property
    def is_active(self):
        return self.is_enabled
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)
    
    def __unicode__(self):
        return self.email

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    
    def __unicode__(self):
        return self.name

class UserRole(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))

class MenuItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)
    category = db.Column(db.String(50))
    stocked_out = db.Column(db.Boolean)
    price = db.Column(db.Float(6))
    description = db.Column(db.String(140))
    image_path = db.Column(db.String(140), unique=True)

    def __unicode__(self):
        return self.name

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(db.DateTime)
    submitted = db.Column(db.Boolean, default=False)
    submitted_on = db.Column(db.DateTime)
    pick_up_date = db.Column(db.DateTime)
    ready_for_pick_up = db.Column(db.Boolean)
    special_instructions = db.Column(db.String(140))
    order_items = db.relationship('OrderItems', 
                                   backref='orders',
                                   cascade='delete, delete-orphan',
                                   lazy='dynamic')

    def order_total(self):
        order_total = 0
        for item in self.order_items:
            order_total += item.menu_item.price
        return order_total

    def __unicode__(self):
        return str(self.user_id)

class OrderItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'))
    side_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'))
    quantity = db.Column(db.Integer)

    menu_item = db.relationship(MenuItems, 
                                foreign_keys=[menu_item_id], 
                                backref="menu_item")
    side_item = db.relationship(MenuItems, 
                                foreign_keys=[side_id], 
                                backref="side_item")

    def __unicode__(self):
        return str(self.id)