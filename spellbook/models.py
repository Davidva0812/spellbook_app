from spellbook import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    #Relationship between the 2 tables:
    spells = db.relationship("Spell", backref="author", lazy=True)

    def __repr__(self):
        return f"User({self.username}, {self.email})"


class Spell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    school = db.Column(db.String, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User({self.name}, {self.author.username})"