from app.main.model.role import Role
import datetime
from app.main import db


def create_role(data):
    name = data['name']
    des = data['description']
    role = Role(name=name, description=des,
                created_at=datetime.datetime.now())
    save_changes(role)
    res_obj = {
        'status': 'success',
        'message': 'Role is created',
        'role_name': name,
        'role_description': des
    }
    return res_obj,201


def get_all_role():
    Role.query.all()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
