from flask import request
from flask_restplus import Resource
from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, user_login
from ..service.permission_service import get_permission_by_id
from ..service.role_service import get_role_by_id
from flask_jwt_extended import jwt_required, get_jwt_identity

api = UserDto.api
_user = UserDto.user
_userLogin = UserDto.userLogin


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/token')
@api.response(403, 'Wrong credentials')
class UserLogin(Resource):
    @api.expect(_userLogin, validate=True)
    def post(self):
        """Login account """
        data = request.json
        return user_login(data['username'], data['password'])


@api.route('/me/info')
@api.response(404, 'User not found.')
class UserInfo(Resource):
    @api.doc('get a user')
    @jwt_required
    @api.marshal_with(_user)
    def get(self):
        """Get account information"""
        public_id = get_jwt_identity()
        user = get_a_user(public_id)
        return user


@api.route('/me/permission')
@api.response(404, 'Permission not found.')
class UserInfo(Resource):
    @api.doc('get permission')
    @jwt_required
    def get(self):
        """Get Permission By Self"""
        public_id = get_jwt_identity()
        return get_permission_by_id(public_id)


@api.route('/me/role')
class User(Resource):
    @api.doc('get role by user')
    @jwt_required
    def get(self):
        """Get Role By Self"""
        public_id = get_jwt_identity()
        user = get_role_by_id(public_id)
        if not user:
            api.abort(404)
        else:
            return user


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user
