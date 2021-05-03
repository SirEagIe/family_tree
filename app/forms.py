from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already taken')


class AddToTreeForm(FlaskForm):
    first_parent = RadioField('First parent', choices=[], default='0')
    second_parent = RadioField('Second parent', choices=[], default='0')
    name = StringField('Name', validators=[DataRequired()])
    is_alive = BooleanField('Alive')
    date_of_birthday = DateField('Birthday')
    date_of_death = DateField('Death')
    description = StringField('Description')
    image = StringField('Image')
    add_submit = SubmitField('Submit')


class RemoveFromTreeForm(FlaskForm):
    humans = RadioField('Remove', choices=[])
    remove_submit = SubmitField('Submit')


class ChangeInTreeForm(FlaskForm):
    humans = RadioField('Change', choices=[])
    first_parent = RadioField('First parent', choices=[], default='0')
    second_parent = RadioField('Second parent', choices=[], default='0')
    name = StringField('Name', validators=[DataRequired()])
    is_alive = BooleanField('Alive')
    date_of_birthday = DateField('Birthday')
    date_of_death = DateField('Death')
    description = StringField('Description')
    image = StringField('Image')
    change_submit = SubmitField('Submit')
