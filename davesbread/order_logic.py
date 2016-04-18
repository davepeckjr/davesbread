from flask import flash, redirect, session, url_for, render_template, request
from flask.ext.user import login_required, current_user, roles_required
from davesbread import davesbread, db#, lm
from .models import MenuItems, Orders, OrderItems
from .forms import OrderForm, EditOrderForm, FinalForm
from .util import send_email
import datetime

def order_loader():
    order_exists = Orders.query.filter_by(user_id=current_user.id).first()
    if order_exists is None or order_exists.submitted:
        return False
    else:
        return True

@davesbread.route('/review_order')
@login_required
def review_order():
    order = Orders.query.filter_by(user_id=current_user.id, submitted=False).first()
    menu_items = OrderItems.query.filter_by(order_id=order.id)
    subtotal = order.order_total()
    return render_template('customer/review.html', 
                            title="Dave's Bread - Review Order",
                            menu_items=menu_items,
                            subtotal=subtotal,
                            user=current_user)

@davesbread.route('/add_to_order/<menu_item_id>', methods=['GET', 'POST'])
@login_required
def add_to_order(menu_item_id):
    id = menu_item_id
    form = OrderForm()
    side = form.side.data
    side_item = MenuItems.query.filter_by(id=int(side)).first()
    quantity = form.quantity.data
    menu_item = MenuItems.query.filter_by(id=id).first()
    order_exists = order_loader()
    if order_exists:
        order = Orders.query.filter_by(user_id=current_user.id).first()
        order_item = OrderItems(menu_item=menu_item, quantity=quantity,
                                side_item=side_item)
        order.order_items.append(order_item)
        db.session.add(order)
        db.session.commit()
    else:
        order_item = OrderItems(menu_item=menu_item, quantity=quantity,
                                side_item=side_item)
        order = Orders(user_id=current_user.id, 
                       created_on=datetime.datetime.now(),
                       submitted=False)
        order.order_items.append(order_item)
        db.session.add(order)
        db.session.commit()
        session['cart'] = True
    flash('Item added to order', 'info')
    return redirect(url_for('menu', category=menu_item.category))

@davesbread.route('/edit_item/<item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = OrderItems.query.get(item_id)
    form = EditOrderForm()
    if request.method=='POST':
        side = form.side.data
        side_item = MenuItems.query.filter_by(id=int(side)).first()
        item.side_item = side_item
        item.quantity = form.quantity.data
        db.session.commit()
        flash('Order Updated', 'info')
        return redirect(url_for('review_order'))
    return render_template('customer/edit_item.html', 
                            title="Dave's Bread - " + item.menu_item.name,
                            item=item, 
                            form=form, 
                            user=current_user)

@davesbread.route('/remove_from_order/<order_item_id>')
@login_required
def remove_from_order(order_item_id):
    order = Orders.query.filter_by(user_id=current_user.id).first()
    OrderItems.query.filter_by(id=order_item_id).delete()
    db.session.commit()
    flash('Item removed from order', 'info')
    return redirect(url_for('review_order'))

@davesbread.route('/submit_order', methods=['GET', 'POST'])
@login_required
def submit_order():
    form = FinalForm()
    order = Orders.query.filter_by(user_id=current_user.id, submitted=False).first()
    order.pick_up_date = form.pick_up_time.data
    order.special_instructions = form.special_instructions.data
    order.submitted=True
    order.submitted_on = datetime.datetime.now()
    db.session.commit()
    session['cart'] = False
    send_email(to=current_user.email, 
				   subject="Dave's Bread Order", 
				   html=render_template('emails/order_confirm.html'))
    flash('Order submitted! A confirmation email will arrive shortly', 'success')
    return redirect(url_for('index'))

@davesbread.route('/finalize', methods=['GET', 'POST'])
@login_required
def finalize():
    form = FinalForm()
    if form.validate_on_submit():
        submit_order()
    return render_template('customer/finalize.html', form=form, user=current_user)

@davesbread.route('/ready/<order_id>')
@login_required
@roles_required('manager')
def ready(order_id):
    order = Orders.query.filter_by(id=order_id).first()
    order.ready_for_pick_up = True
    db.session.commit()
    flash('Order marked ready for pick up', 'info')
    return redirect(url_for('order_details', order_id=order_id))