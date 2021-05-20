from app import app, db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from werkzeug.utils import secure_filename
from app.models import User, Human
import os, sys

def recursion_check(db, id, parents_id):
    if id in parents_id:
        return False
    if len(parents_id) == 0:
        return True
    parents_id_tmp = []
    for parent_id in parents_id:
        parent = db.session.query(Human).filter_by(id=parent_id).first()
        if parent.parent_id_1:
            parents_id_tmp.append(parent.parent_id_1)
        if parent.parent_id_2:
            parents_id_tmp.append(parent.parent_id_2)
    return recursion_check(db, id, parents_id_tmp)


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(message='Это поле должно быть заполнено')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Это поле должно быть заполнено')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(message='Это поле должно быть заполнено')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Это поле должно быть заполнено')])
    password_repeat = PasswordField('Повторите пароль', validators=[DataRequired(message='Это поле должно быть заполнено'), EqualTo('password', message='Пароли не совпадают')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Данное имя уже занято')


class AddToTreeForm(FlaskForm):
    first_parent = RadioField('First parent', choices=[], default='0')
    second_parent = RadioField('Second parent', choices=[], default='0')
    name = StringField('Name', validators=[DataRequired()])
    is_alive = BooleanField('Alive')
    date_of_birthday = DateField('Birthday')
    date_of_death = DateField('Death')
    description = TextAreaField('Description')
    image = FileField('image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    add_submit = SubmitField('Submit')

    def addChoices(self, choices):
        self.first_parent.choices = choices
        self.second_parent.choices = choices

    def addHumanInDb(self, db, user_id):
        if self.image.data:
            filename = secure_filename(self.image.data.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            self.image.data.save(file_path)
        else:
            filename = 'default.png'
        user = User.query.filter_by(id=user_id).first()
        human = Human(name = self.name.data,
                      parent_id_1 = self.first_parent.data,
                      parent_id_2 = self.second_parent.data,
                      is_alive = self.is_alive.data,
                      date_of_birthday = self.date_of_birthday.data,
                      description = self.description.data,
                      image = os.path.join('static/photo', filename),
                      author = user)
        if not self.is_alive.data:
            human.date_of_death = self.date_of_death.data
        db.session.add(human)
        db.session.commit()
        parents = []
        if int(human.parent_id_1):
            parents.append(human.parent_id_1)
        if int(human.parent_id_2):
            parents.append(human.parent_id_2)
        if not recursion_check(db, human.id, parents):
            db.session.delete(human)
            db.session.commit()
            # ???
            self.errors.add_submit.append('Невозможно отобразить данные')

class RemoveFromTreeForm(FlaskForm):
    humans = RadioField('Remove', choices=[])
    remove_submit = SubmitField('Submit')

    def addChoices(self, choices):
        self.humans.choices = choices[1:]

    def removeHumanFromDb(self, db):
        human = Human.query.filter_by(id=self.humans.data).first()
        db.session.delete(human)
        db.session.query(Human).filter_by(parent_id_1=self.humans.data).update({Human.parent_id_1: 0})
        db.session.query(Human).filter_by(parent_id_2=self.humans.data).update({Human.parent_id_2: 0})
        db.session.commit()


class ChangeInTreeForm(FlaskForm):
    humans = RadioField('Change', choices=[])
    first_parent = RadioField('First parent', choices=[], default='0')
    second_parent = RadioField('Second parent', choices=[], default='0')
    name = StringField('Name', validators=[DataRequired()])
    is_alive = BooleanField('Alive')
    date_of_birthday = DateField('Birthday')
    date_of_death = DateField('Death')
    description = TextAreaField('Description')
    image = FileField('image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    change_submit = SubmitField('Submit')

    def addChoices(self, choices):
        self.humans.choices = choices[1:]
        self.first_parent.choices = choices
        self.second_parent.choices = choices
        if len(choices) > 1:
            self.humans.default = choices[1][0]

    def changeHumanInDb(self, db):
        parents = []
        if int(self.first_parent.data):
            parents.append(int(self.first_parent.data))
        if int(self.second_parent.data):
            parents.append(int(self.second_parent.data))
        if not recursion_check(db, int(self.humans.data), parents):
            # ???
            self.change_submit.errors.append('Невозможно отобразить данные')
            return
        update_dict = {Human.name: self.name.data,
                       Human.parent_id_1: self.first_parent.data,
                       Human.parent_id_2: self.second_parent.data,
                       Human.is_alive: self.is_alive.data,
                       Human.date_of_birthday: self.date_of_birthday.data,
                       Human.description: self.description.data}
        if self.image.data:
            filename = secure_filename(self.image.data.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            self.image.data.save(file_path)
            update_dict[Human.image] = os.path.join(app.config['PHOTO_FOLDER'], filename)
        if self.is_alive.data:
            update_dict[Human.date_of_death] = None
        else:
            update_dict[Human.date_of_death] = self.date_of_death.data
        db.session.query(Human).filter_by(id=self.humans.data).update(update_dict)
        db.session.commit()
