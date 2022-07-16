from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from . import models
from . import forms
from . import login_manager


# post functions

def index():
    customers = models.Customer.query.all()
    return render_template('index.html', customers=customers)

@login_required
def customer_create():
    form = forms.CustomerForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            customer = models.Customer(name=request.form.get('name'),
                                       phone_number=request.form.get('phone_number'),
                                       item=request.form.get('item'),
                                       quantity=request.form.get('quantity'),
                                       price=request.form.get('price'),
                                       user_id=current_user.id)
            db.session.add(customer)
            db.session.commit()
            flash('Покупка добавлена', category='success')
            return redirect(url_for('index'))
        elif form.errors:
            for errors in form.errors.values():
                for error in errors:
                    flash(error, category='danger')
    return render_template('customer_create.html', form=form)


def customer_detail(customer_id):
    customer = models.Customer.query.filter_by(id=customer_id).first()
    return render_template('customer_detail.html', customer=customer)

@login_required
def customer_delete(customer_id):
    customer = models.Customer.query.filter_by(id=customer_id).first()
    form = forms.CustomerForm(obj=customer)
    if customer:
        if customer.user_id == current_user.id:
            if request.method == 'POST':
                db.session.delete(customer)
                db.session.commit()
                flash('Покупка удалена', category='success')
                return redirect(url_for('index'))
            else:
                return render_template('customer_delete.html', customer=customer, form=form)
        else:
            flash('Нет прав на удаление', category='danger')
            return redirect(url_for('index'))
    else:
        flash('Покупка не найдена', category='danger')
        return redirect(url_for('index'))

@login_required
def customer_update(customer_id):
    customer = models.Customer.query.filter_by(id=customer_id).first()
    if customer:
        if customer.user_id == current_user.id:
            form = forms.CustomerForm(obj=customer)
            if request.method == 'POST':
                if form.validate_on_submit():
                    name = request.form.get('name'),
                    phone_number = request.form.get('phone_number'),
                    item = request.form.get('item'),
                    quantity = request.form.get('quantity'),
                    price = request.form.get('price'),
                    customer.name = name
                    customer.phone_number = phone_number
                    customer.item = item
                    customer.quantity = quantity
                    customer.price = price
                    db.session.commit()
                    flash('Новость обновлена', category='succes')
                    return redirect(url_for('index'))
                if form.errors:
                    for errors in form.errors.values():
                        for error in errors:
                            flash(error, category='danger')

            return render_template('post_edit.html', customer=customer, form=form)
        else:
            flash('У вас недостаточно прав', category='danger')
            return redirect(url_for('index.html'))
    else:
        flash('Новость не найдена', category='danger')
        return redirect(url_for('index.html'))


# user functions

def register():
    form = forms.UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = models.User(username=request.form.get('username'), password=request.form.get('password'))
            db.session.add(user)
            db.session.commit()
            flash('Вы успешно зарегистрировались!', category='success')
            return redirect(url_for('login'))
        elif form.errors:
            for errors in form.errors.values():
                for error in errors:
                    flash(error, category='danger')
    return render_template('register.html', form=form)


def login():
    form = forms.UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = models.User.query.filter_by(username=request.form.get('username')).first()
            if user and user.check_password(request.form.get('password')):
                login_user(user)
                flash('Вы вошли', category='success')
                return redirect(url_for('index'))
            else:
                flash('Неверный логин или пароль', category='danger')
        elif form.errors:
            for errors in form.errors.values():
                for error in errors:
                    flash(error, category='danger')
    return render_template('login.html', form=form)


def logout():
    logout_user()
    flash('Вы вышли из учетной записи', category='success')
    return redirect(url_for('index'))