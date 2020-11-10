from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user_profile', {
        'full_name': fields.String(required=True, description='Họ và tên'),
        'email': fields.String(required=True, description='Địa chỉ email'),
        'username': fields.String(required=True, description='Tên đăng nhập'),
        'password': fields.String(required=True, description='Mật khẩu'),
        'public_id': fields.String(description='Mã người dùng'),
        'registered_on': fields.String(description='Ngày tạo'),
        'is_active': fields.Boolean(description='Trạng thái kích hoạt')
    })

    userLogin = api.model('user_login', {
        'username': fields.String(required=True, description='Tên đăng nhập'),
        'password': fields.String(required=True, description='Mật khẩu'),
    })


class RoleDto:
    api = Namespace('role', description='roles')
    role = api.model('role', {
        'id': fields.Integer(required=True, description='Mã vai trò'),
        'name': fields.String(required=True, description='Tên vai trò'),
        'description': fields.String(required=True, description='Mô tả vai trò'),
        # 'created_at': fields.String(required=True, description='Ngày tạo vai trò'),
    })

    role_create = api.model('role', {
        'name': fields.String(required=True, description='Tên vai trò'),
        'description': fields.String(required=True, description='Mô tả vai trò'),
        # 'created_at': fields.String(required=True, description='Ngày tạo vai trò'),
    })

    set_role = api.model('role', {
        'role_id': fields.Arbitrary(required=True, description='Mã vai trò'),
    })


class PermissionDto:
    api = Namespace('permission', description='permissions')
    permission = api.model('permission', {
        'id': fields.Integer(required=True, description='Mã quyền truy cập'),
        'name': fields.String(required=True, description='Tên quyền truy cập'),
        'description': fields.String(required=True, description='Mô tả quyền truy cập'),
        # 'created_at': fields.String(required=True, description='Ngày tạo vai trò'),
    })

    permission_create = api.model('permission', {
        'name': fields.String(required=True, description='Tên quyền truy cập'),
        'description': fields.String(required=True, description='Mô tả quyền truy cập'),
        # 'created_at': fields.String(required=True, description='Ngày tạo vai trò'),
    })

    set_role = api.model('permission', {
        'permission_id': fields.Arbitrary(required=True, description='Mã quyền truy cập'),
    })
