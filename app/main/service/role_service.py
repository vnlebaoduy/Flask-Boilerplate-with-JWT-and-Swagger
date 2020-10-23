from app.main.model.role import Role
import datetime
from app.main import db
from app.main.model.user import User
from flask_jwt_extended import get_jwt_identity


def create_role(data):
    public_id = get_jwt_identity()
    name = data['name'].strip()
    des = data['description']
    check_role = Role.query.filter_by(name=name).first()
    if not check_role:
        user = User.query.filter_by(public_id=public_id).first()
        role = Role(name=name, description=des,
                    created_at=datetime.datetime.now(), created_by=user.username)
        save_changes(role)
        res_obj = {
            'status': 'success',
            'message': 'Role is created',
            'role_name': name,
            'role_description': des
        }
        return res_obj, 201
    else:
        res_obj = {
            'status': 'conflict',
            'message': 'Role {} already exists.'.format(name),
        }
        return res_obj, 409


def delete_role_id(role_id):
    role = Role.query.filter_by(id=role_id).first()
    if role:
        delete_changes(role)
        res_obj = {
            'status': 'success',
            'message': 'Role {} deleted.'.format(role.name),
        }
        return res_obj, 200
    else:
        res_obj = {
            'status': 'failure',
            'message': 'Role id={} not found.'.format(role_id),
        }
        return res_obj, 404


def get_all_role():
    role = Role.query.all()
    return role


def delete_changes(data):
    db.session.delete(data)
    db.session.commit()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
