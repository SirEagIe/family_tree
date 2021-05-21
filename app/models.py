from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    human = db.relationship('Human', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<id: {}, username: {}>'.format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Human(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(('user.id')), index=True)
    name = db.Column(db.String(64))
    parent_id_1 = db.Column(db.Integer)
    parent_id_2 = db.Column(db.Integer)
    is_alive = db.Column(db.Boolean)
    date_of_birthday = db.Column(db.Date)
    date_of_death = db.Column(db.Date)
    description = db.Column(db.String(512))
    image = db.Column(db.String(256))

    def __repr__(self):
        return '<id: {}, user_id: {}, name: {}; p1: {}, p2: {}>'.format(self.id,
                    self.user_id, self.name, self.parent_id_1, self.parent_id_2)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
