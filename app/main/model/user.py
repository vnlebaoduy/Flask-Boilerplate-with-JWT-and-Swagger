from .. import db, flask_bcrypt, ma
from sqlalchemy import Table, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime
from ..model.role import Role


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    public_id = db.Column(db.String(100), unique=True)
    full_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, unique=False, default=True)
    role = db.relationship('Role', secondary='user_role')

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{} - {} - {} - {}'>".format(self.username, self.email, self.public_id, self.registered_on)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


class UserRole(db.Model):
    __tablename__ = 'user_role'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    user = db.relationship(User, backref=db.backref("role_user_assoc"))
    role = db.relationship(Role, backref=db.backref("user_role_assoc"))

    def __repr__(self):
        return "<UserRole '{} - {} - {} - {}'>".format(self.user_id, self.role_id, self.created_at, self.created_by)
