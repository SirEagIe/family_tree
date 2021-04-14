from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
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
    description = StringField('Description')
    image = StringField('Image')
    submit = SubmitField('Submit')

class RemoveFromTreeForm(FlaskForm):
    human = RadioField('Remove', choices=[], default='0')
    submit = SubmitField('Submit')

class ChangeHumanInTreeForm(FlaskForm):
    first_parent = RadioField('First parent', choices=[], default='0')
    second_parent = RadioField('Second parent', choices=[], default='0')
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    image = StringField('Image')
    submit = SubmitField('Submit')
