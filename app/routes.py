from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddToTreeForm, RemoveFromTreeForm, ChangeInTreeForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Human
from werkzeug.urls import url_parse
import sys
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
            flash('Invalid username or password')
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
        flash('Congratulations, you are now a registered user!')
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
    choices_without_nobody = [] # TODO: найти решение получше
    for human in humans:
        choices.append((human.id, human.name+' (' + str(human.date_of_birthday) + ')'))
        choices_without_nobody.append((human.id, human.name+' (' + str(human.date_of_birthday) + ')'))
    add_form.first_parent.choices = choices
    add_form.second_parent.choices = choices
    remove_form.humans.choices = choices_without_nobody
    change_form.humans.choices = choices_without_nobody
    change_form.first_parent.choices = choices
    change_form.second_parent.choices = choices
    change_form.humans.default = choices_without_nobody[0][0]
    if add_form.add_submit.data and add_form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        human = Human(name = add_form.name.data,
                      parent_id_1 = add_form.first_parent.data,
                      parent_id_2 = add_form.second_parent.data,
                      is_alive = add_form.is_alive.data,
                      date_of_birthday = add_form.date_of_birthday.data,
                      description = add_form.description.data,
                      image = add_form.image.data,
                      author = user)
        if not add_form.is_alive.data:
            human.date_of_death = add_form.date_of_death.data
        db.session.add(human)
        db.session.commit()
        return redirect(url_for('tree'))
    if remove_form.remove_submit.data and remove_form.validate_on_submit():
        human = Human.query.filter_by(id=remove_form.humans.data).first()
        db.session.delete(human)
        db.session.query(Human).filter_by(parent_id_1=remove_form.humans.data).update({Human.parent_id_1: 0})
        db.session.query(Human).filter_by(parent_id_2=remove_form.humans.data).update({Human.parent_id_2: 0})
        db.session.commit()
        return redirect(url_for('tree'))
    if change_form.change_submit.data and change_form.validate_on_submit():
        update_dict = {Human.name: change_form.name.data,
                       Human.parent_id_1: change_form.first_parent.data,
                       Human.parent_id_2: change_form.second_parent.data,
                       Human.is_alive: change_form.is_alive.data,
                       Human.date_of_birthday: change_form.date_of_birthday.data,
                       Human.description: change_form.description.data,
                       Human.image: change_form.image.data}
        if change_form.is_alive.data:
            update_dict[Human.date_of_death] = None
        else:
            update_dict[Human.date_of_death] = change_form.date_of_death.data
        db.session.query(Human).filter_by(id=change_form.humans.data).update(update_dict)
        db.session.commit()
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
        temp_data['description'] = human.description + ' ' + str(human.date_of_birthday)
        if not human.is_alive:
            temp_data['description'] += ' - ' + str(human.date_of_death)
        else:
            temp_data['description'] += ' - ...'
        temp_data['image'] = human.image
        data.append(temp_data)
    return render_template('tree.html', data=data, add_form=add_form,
                           remove_form=remove_form, change_form=change_form)
