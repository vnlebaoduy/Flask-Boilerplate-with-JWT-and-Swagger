from flask import request
from flask_restplus import Resource, reqparse
from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, user_login
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.main.util.decorator import admin_token_required

api = UserDto.api
_user = UserDto.user
_userLogin = UserDto.userLogin


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
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
@api.expect(_userLogin, validate=True)
class UserLogin(Resource):
    def post(self):
        data = request.json
        return user_login(data['username'], data['password'])


@api.route('/info/me')
@api.response(404, 'User not found.')
class UserInfo(Resource):
    @api.doc('get a user')
    @jwt_required
    @api.marshal_with(_user)
    def get(self):
        public_id = get_jwt_identity()
        user = get_a_user(public_id)
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


@api.route('/role')
class User(Resource):
    @api.doc('get role by user')
    def get(self, public_id):
        """get role by user"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user
