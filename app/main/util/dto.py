from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='Địa chỉ email'),
        'username': fields.String(required=True, description='Tên đăng nhập'),
        'password': fields.String(required=True, description='Mật khẩu'),
        'public_id': fields.String(description='Mã người dùng'),
        'registered_on': fields.String(description='Ngày tạo'),
        'is_active': fields.Boolean(description='Trạng thái kích hoạt')
    })

    userLogin = api.model('user', {
        'username': fields.String(required=True, description='Tên đăng nhập'),
        'password': fields.String(required=True, description='Mật khẩu'),
    })


class RoleDto:
    api = Namespace('role', description='roles')
    role = api.model('role', {
        'name': fields.String(required=True, description='Tên vai trò'),
        'description': fields.String(required=True, description='Mô tả vai trò'),
        # 'created_at': fields.String(required=True, description='Ngày tạo vai trò'),
    })
