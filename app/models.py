from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    peoples_in_trees = db.relationship('Peoples_in_trees', backref='author', lazy='dynamic')

def __repr__(self):
    return '<User {}'.format(self.username)


class Peoples_in_trees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey(('user.id')), index=True)

    def __repr__(self):
        return '<Name {}'.format(self.name)
