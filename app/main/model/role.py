from .. import db, flask_bcrypt, ma
import datetime


class Role(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), unique=False, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    user = db.relationship("User", secondary='user_role')
    permission = db.relationship("Permission", secondary='role_permission')


class RolePermission(db.Model):
    __tablename__ = 'role_permission'

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True, )
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), primary_key=True, )
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    role = db.relationship(Role, backref=db.backref("permission_role_assoc"))
    permission = db.relationship('Permission', backref=db.backref("role_permission_assoc"))


class RoleSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "description")
