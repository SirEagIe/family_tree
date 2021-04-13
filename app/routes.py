from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddToTreeForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Human
from werkzeug.urls import url_parse

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

@app.route('/tree')
@login_required
def tree():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    humans = db.session.query(Human).filter(Human.user_id == current_user.id).all();
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
        temp_data['description'] = human.description
        temp_data['image'] = human.image
        data.append(temp_data)
    return render_template('tree.html', data=data)

@app.route('/add_to_tree', methods=['GET', 'POST'])
def add_to_tree():
    form = AddToTreeForm()
    humans = db.session.query(Human).filter(Human.user_id == current_user.id).all();
    choices = [('0', 'Nobody')]
    for human in humans:
        choices.append((human.id, human.name))
    form.first_parent.choices = choices
    form.second_parent.choices = choices
    if form.validate_on_submit():
        flash(form.first_parent.data + ' ' + form.second_parent.data + ' ' + form.name.data)
        return redirect(url_for('index'))
    return render_template('add_to_tree.html', form=form)
