from app.main.model.role import Role, RoleSchema
from app.main import db
from app.main.model.user import User, UserRole
from flask_jwt_extended import get_jwt_identity


def create_role(data):
    public_id = get_jwt_identity()
    name = data['name'].strip()
    des = data['description'].strip()
    check_role = Role.query.filter_by(name=name).first()
    if not check_role:
        user = User.query.filter_by(public_id=public_id).first()
        role = Role(name=name, description=des, created_by=user.username)
        save_changes(role)
        res_obj = {
            'status': 'success',
            'message': 'Role is created',
            'name': name,
            'description': des
        }
        return res_obj, 201
    else:
        res_obj = {
            'status': 'fail',
            'message': 'Role {} already exists.'.format(name),
        }
        return res_obj, 409


def update_role_by_id(data):
    id_role = data['id']
    name = data['name'].strip()
    des = data['description'].strip()
    if len(name) <= 0:
        res_obj = {
            'status': 'fail',
            'message': 'param "name" is missing',
        }
        return res_obj, 422
    elif len(des) <= 0:
        res_obj = {
            'status': 'fail',
            'message': 'param "description" is missing',
        }
        return res_obj, 422
    else:
        role = Role.query.filter_by(id=id_role).first()
        role.name = name
        role.description = des
        save_changes(role)
        res_obj = {
            'status': 'success',
            'name': name,
            'description': des
        }
        return res_obj, 200


def delete_role_id(role_id):
    role = Role.query.filter_by(id=role_id).first()
    if role:
        delete_changes(role)
        res_obj = {
            'status': 'success',
            'message': 'Role {} has been deleted.'.format(role.name),
        }
        return res_obj, 200
    else:
        res_obj = {
            'status': 'fail',
            'message': 'Role id={} not found.'.format(role_id),
        }
        return res_obj, 404


def get_all_role():
    role = Role.query.all()
    roles_schema = RoleSchema(many=True)
    res_data = roles_schema.dump(role)
    res_obj = {
        'status': 'success',
        'data': res_data
    }
    return res_obj


def get_role_by_id(public_id):
    list_role = db.session.query(Role).join(UserRole).join(User).filter(
        User.public_id == public_id).all()
    roles_schema = RoleSchema(many=True)
    res_data = roles_schema.dump(list_role)
    res_obj = {
        'status': 'success',
        'data': res_data
    }
    return res_obj


def set_role_user_by_ids(role_id, public_id):
    public_id_creator = get_jwt_identity()
    user_creator = User.query.filter_by(public_id=public_id_creator).first()
    user = User.query.filter_by(public_id=public_id).first()

    get_user_role = UserRole.query.filter_by(role_id=role_id).filter_by(user_id=user.id).first()
    if not get_user_role:
        role = Role.query.filter_by(id=role_id).first()

        user_role_add = UserRole(user=user, role=role, created_by=user_creator.username)
        save_changes(user_role_add)

        list_role_2 = db.session.query(Role).join(UserRole).join(User).filter(UserRole.user_id == user.id).all()
        roles_schema = RoleSchema(many=True)
        res_data = roles_schema.dump(list_role_2)
        res_obj = {
            'status': 'success',
            'roles': res_data
        }
        return res_obj, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Role already exists!',
        }
        return response_object, 409


def delete_changes(data):
    db.session.delete(data)
    db.session.commit()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
