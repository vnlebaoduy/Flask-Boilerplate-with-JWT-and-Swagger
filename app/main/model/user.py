from .. import db, flask_bcrypt
from sqlalchemy import Table, Integer, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
user_role_table = db.Table('user_role',
                           db.Column('id',db.Integer, primary_key=True, autoincrement=True),
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                           db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, unique=False, default=True)
    role = db.relationship('Role', secondary=user_role_table,
                                backref=db.backref('user_role', lazy='dynamic'))

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
