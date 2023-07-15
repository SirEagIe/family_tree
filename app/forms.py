from app import app, db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField
from wtforms.fields import DateField
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
    add_first_parent = RadioField('Первый родитель', choices=[], default='0')
    add_second_parent = RadioField('Второй родитель', choices=[], default='0')
    name = StringField('Имя', validators=[DataRequired('Это поле должно быть заполнено')])
    is_alive = BooleanField('Жив')
    date_of_birthday = DateField('Дата рождения', validators=[DataRequired()])
    date_of_death = DateField('Дата смерти')
    description = TextAreaField('Описание')
    image = FileField('Фото', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    add_submit = SubmitField('Добавить')

    def addChoices(self, choices):
        self.add_first_parent.choices = choices
        self.add_second_parent.choices = choices

    def addHumanInDb(self, db, user_id):
        if self.image.data:
            filename = secure_filename(self.image.data.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            self.image.data.save(file_path)
        else:
            filename = 'default.png'
        user = User.query.filter_by(id=user_id).first()
        human = Human(name = self.name.data,
                      parent_id_1 = self.add_first_parent.data,
                      parent_id_2 = self.add_second_parent.data,
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

class RemoveFromTreeForm(FlaskForm):
    remove_humans_list = RadioField('Удалить', choices=[])
    remove_submit = SubmitField('Удалить')

    def addChoices(self, choices):
        self.remove_humans_list.choices = choices[1:]

    def removeHumanFromDb(self, db):
        human = Human.query.filter_by(id=self.remove_humans_list.data).first()
        db.session.delete(human)
        db.session.query(Human).filter_by(parent_id_1=self.remove_humans_list.data).update({Human.parent_id_1: 0})
        db.session.query(Human).filter_by(parent_id_2=self.remove_humans_list.data).update({Human.parent_id_2: 0})
        db.session.commit()


class ChangeInTreeForm(FlaskForm):
    change_humans_list = RadioField('Изменить', choices=[])
    change_first_parent = RadioField('Первый родитель', choices=[], default='0')
    change_second_parent = RadioField('Второй родитель', choices=[], default='0')
    name = StringField('Имя', validators=[DataRequired('Это поле должно быть заполнено')])
    is_alive = BooleanField('Жив')
    date_of_birthday = DateField('Дата рождения', validators=[DataRequired()])
    date_of_death = DateField('Дата смерти')
    description = TextAreaField('Описание')
    image = FileField('Фото', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    change_submit = SubmitField('Изменить')

    def addChoices(self, choices):
        self.change_humans_list.choices = choices[1:]
        self.change_first_parent.choices = choices
        self.change_second_parent.choices = choices
        if len(choices) > 1:
            self.change_humans_list.default = choices[1][0]

    def changeHumanInDb(self, db):
        parents = []
        if int(self.change_first_parent.data):
            parents.append(int(self.change_first_parent.data))
        if int(self.change_second_parent.data):
            parents.append(int(self.change_second_parent.data))
        if not recursion_check(db, int(self.change_humans_list.data), parents):
            return
        update_dict = {Human.name: self.name.data,
                       Human.parent_id_1: self.change_first_parent.data,
                       Human.parent_id_2: self.change_second_parent.data,
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
        db.session.query(Human).filter_by(id=self.change_humans_list.data).update(update_dict)
        db.session.commit()
