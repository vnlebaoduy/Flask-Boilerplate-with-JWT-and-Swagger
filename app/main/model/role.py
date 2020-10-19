from .. import db, flask_bcrypt

role_permission = db.Table('role_permission',
                           db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                           db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                           db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')))


class Role(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), unique=False, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    permission = db.relationship('Permission', secondary=role_permission,
                                 backref=db.backref('role', lazy='dynamic'))
