import datetime
from flask import render_template, request, flash, session, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from davesbread import davesbread, db#, lm
from .models import MenuItems, User
from order_logic import order_loader, add_to_order
from forms import LoginForm, SignupForm, OrderForm

@davesbread.route('/', methods=['GET', 'POST'])
@davesbread.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('customer/index.html', 
                            title="Dave's Bread - Home", user=current_user)

@davesbread.route('/menu/<category>')
def menu(category):
    if category == 'all':
        menu_items=MenuItems.query.all()
    else:
            menu_items = MenuItems.query.filter_by(category=category).all()
    return render_template('customer/menu.html', title="Dave's Bread - Menu", 
                            menu_items=menu_items, user=current_user)

@davesbread.route('/detail/<menu_item_name>', methods=['GET', 'POST'])
def detail(menu_item_name):
    form = OrderForm()
    menu_item = MenuItems.query.filter_by(name=menu_item_name).first_or_404()
    if form.validate_on_submit():
        add_to_order(menu_item.id)
    return render_template('customer/detail.html', title="Dave's Bread - " + menu_item.name,
                            menu_item=menu_item, form=form, user=current_user)

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

@davesbread.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))

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
