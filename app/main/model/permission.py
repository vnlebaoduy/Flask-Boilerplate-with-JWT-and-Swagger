from .. import db, flask_bcrypt, ma
import datetime


class Permission(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), unique=False, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    role = db.relationship("Role", secondary='role_permission')


class PermissionSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "created_at")
