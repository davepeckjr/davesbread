from flask import flash, redirect, url_for, render_template
from flask.ext.user import roles_required, login_required, current_user
from davesbread import davesbread, db
from .models import User, Orders, MenuItems, OrderItems
from .forms import ContactCustomerForm
from .util import send_email

@davesbread.route('/manager')
@roles_required('manager')
@login_required
def manager():
    return render_template('manager/manager_index.html')

@davesbread.route('/manager/current_orders')
@roles_required('manager')
@login_required
def current_orders():
    orders = Orders.query.filter_by(submitted=True).all()
    return render_template('manager/current_orders.html',
                             orders=orders,
                             user=current_user)

@davesbread.route('/manager/order_details/<order_id>')
@roles_required('manager')
@login_required
def order_details(order_id):
    order = Orders.query.filter_by(id=order_id).first()
    menu_items = OrderItems.query.filter_by(order_id=order.id).all()
    return render_template('manager/order_details.html', 
                            order=order,
                            menu_items=menu_items)

@davesbread.route('/manager/contact_customer')
@login_required
@roles_required('manager')
def contact_customer():
    form = ContactCustomerForm()
    if form.validate_on_submit():
        email_customer(current_user.id)
    return render_template('manager/contact_customer.html', 
                            user=current_user, 
                            form=form)

@davesbread.route('/manager/stock_out')
@login_required
@roles_required('manager')
def stock_out():
    return render_template('manager/stock_out.html')

@davesbread.route('/manager/search_orders')
@login_required
@roles_required('manager')
def search_orders():
    return render_template('manager/search_orders.html')

@davesbread.route('/manager/email_customer/<id>', methods=['GET', 'POST'])
@login_required
@roles_required('manager')
def email_customer(id):
    form = ContactCustomerForm()
    body = form.body.data
    user = User.query.filter_by(id=id).first()
    send_email(to=user.email,
			   subject="We got a quick question for you",
			   html=render_template('emails/email_customer.html', 
									 body=body)
			   )
    flash('Email sent.')
    return redirect(url_for('current_orders'))