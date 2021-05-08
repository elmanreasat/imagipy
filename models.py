from db import db
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

login = LoginManager()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(1000))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Img(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, )
    user_id = db.Column(db.Integer, nullable=False)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))