from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddToTreeForm, RemoveFromTreeForm, ChangeInTreeForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Human
from werkzeug.urls import url_parse
import sys, os

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный логин или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/tree', methods=['GET', 'POST'])
@login_required
def tree():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    humans = db.session.query(Human).filter_by(user_id=current_user.id).all();
    add_form = AddToTreeForm()
    remove_form = RemoveFromTreeForm()
    change_form = ChangeInTreeForm()
    choices = [('0', 'Nobody')]
    for human in humans:
        choices.append((human.id, human.name+' (' + str(human.date_of_birthday) + ')'))
    add_form.addChoices(choices)
    remove_form.addChoices(choices)
    change_form.addChoices(choices)
    if add_form.add_submit.data and add_form.validate_on_submit():
        add_form.addHumanInDb(db, current_user.id)
        return redirect(url_for('tree'))
    if remove_form.remove_submit.data and remove_form.validate_on_submit():
        remove_form.removeHumanFromDb(db)
        return redirect(url_for('tree'))
    if change_form.change_submit.data and change_form.validate_on_submit():
        change_form.changeHumanInDb(db)
        return redirect(url_for('tree'))
    change_form.process()
    data = []
    for human in humans:
        temp_data = {}
        temp_data['parents'] = []
        temp_data['id'] = human.id
        temp_data['name'] = human.name
        if human.parent_id_1:
            temp_data['parents'].append(human.parent_id_1)
        if human.parent_id_2:
            temp_data['parents'].append(human.parent_id_2)
        temp_data['is_alive'] = human.is_alive
        temp_data['date_of_birthday'] = human.date_of_birthday
        temp_data['date_of_death'] = human.date_of_death
        temp_data['description'] = human.description
        temp_data['image'] = human.image
        data.append(temp_data)
    return render_template('tree.html', data=data, add_form=add_form,
                           remove_form=remove_form, change_form=change_form)
