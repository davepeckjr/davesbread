class SubmittedOrders(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    customer_email = db.Column(db.String(120))
    is_complete = db.Column(db.Boolean)
    recieved_on = db.Column(db.DateTime)
    pickup_time = db.Column(db.DateTime)
    
    def __str__(self):
        return '<Order for %r>' % self.customer_email

class Manager(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(64), index=True, unique=False)
    lastname = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)
    
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
    
    @property
    def is_authenticated(self):
        return True
        
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)
    
    def __str__(self):
        return '<Manager %r>' % self.email

@login_required
@davesbread.route('/order/<id>')
def order(id):
    ordered_item = MenuItems.query.filter_by(id=id).first()
if 'cart' in session:
    session['cart'].append({ordered_item.id : current_user.email})
else:
    session['cart'] = [{ordered_item.id : current_user.email}]
flash('Item added to order')
return redirect(url_for('menu', category='all'))

    order=Orders(customer_id=current_user.id,
                 created_on=datetime.datetime.now(),
                 submitted=False)
    db.session.add(order)
    db.session.commit()
    order_id = 
    order_item=OrderItem(order_id=order_id, menu_item_id=menu_item.id,
                         quantity=1)
    db.session.add(order_item)
    db.session.commit()
    if 'cart' not in session:
        session['cart'] = True
    flash("Added to cart")
    return redirect(url_for('detail', menu_item_name=menu_item.name))
    
@login_required
@davesbread.route('/review_order')
def review_order():
    order = Orders.query.filter_by(customer_id=current_user.id).first()
    menu_ids = []
    for item in OrderItems.query.filter_by(order_id=order.id):
        menu_ids.append(item.menu_item)
    items = MenuItems.query.filter(MenuItems.id.in_(menu_ids)).all()
    return render_template('customer/review.html', 
                            title="Dave's Bread - Review Order",
                            items=items, user=current_user)


@login_required
@davesbread.route('/review_order')
def review_order():
    order = Orders.query.filter_by(customer_id=current_user.id).first()
    menu_items = db.session.query(OrderItems, MenuItems).\
                            join(MenuItems, OrderItems.menu_item).\
                            all()
    sides = db.session.query(OrderItems, MenuItems).\
                       join(MenuItems, OrderItems.side_item).\
                       all()
    return render_template('customer/review.html', 
                            title="Dave's Bread - Review Order",
                            menu_items=menu_items,
                            sides=sides, 
                            user=current_user)
                            
"""
@davesbread.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user.check_password(form.password.data):
            login_user(user)
            order_exists = order_loader()
            if order_exists:
                session['cart'] = True
            if 'manager' in user.roles:
                return redirect(url_for('manager'))
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('customer/login.html', form=form, user=current_user, 
                            title="Dave's Bread - Login")
"""

"""
@davesbread.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user=User(firstname=form.firstname.data,
                  lastname=form.lastname.data,
                  email=form.email.data,
                  password=form.password.data)
        user.registered_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('customer/signup.html', form=form, user=current_user, 
                            title="Dave's Bread - Sign Up")
"""