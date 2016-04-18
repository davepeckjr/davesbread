import datetime
from flask import render_template, request, flash, session, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from davesbread import davesbread, db#, lm
from .models import MenuItems, User
from order_logic import order_loader, add_to_order
from forms import LoginForm, UpdateProfileForm, OrderForm

@davesbread.route('/', methods=['GET', 'POST'])
@davesbread.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('customer/index.html', 
                            title="Dave's Bread - Home", user=current_user)

@davesbread.route('/menu/<category>')
def menu(category):
    if category == 'all':
        menu_items=MenuItems.query.filter_by(stocked_out=False).all()
    else:
        menu_items = MenuItems.query.filter_by(category=category, stocked_out=False).all()
    return render_template('customer/menu.html', title="Dave's Bread - Menu", 
                            menu_items=menu_items, user=current_user)

@davesbread.route('/detail/<menu_item_name>', methods=['GET', 'POST'])
def detail(menu_item_name):
    form = OrderForm()
    form.side.choices= [(s.id, s.name) for s in\
                         MenuItems.query.filter_by(category='side').all()]
    menu_item = MenuItems.query.filter_by(name=menu_item_name).first_or_404()
    if form.validate_on_submit():
        add_to_order(menu_item.id)
    return render_template('customer/detail.html', title="Dave's Bread - " + menu_item.name,
                            menu_item=menu_item, form=form, user=current_user)

@davesbread.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))

@davesbread.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    user = User.query.filter_by(id=current_user.id).first()
    form = UpdateProfileForm()
    if request.method=='POST':
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.phone_num = form.phone_num.data
        db.session.commit()
        flash('Profile updated')
        return redirect(url_for('index'))
    return render_template('flask_user/user_profile.html', form=form)

@davesbread.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@davesbread.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500