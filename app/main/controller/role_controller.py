from flask import request
from flask_restplus import Resource,reqparse
from ..service.role_service import get_all_role,create_role
from flask_jwt_extended import jwt_required
from app.main.util.decorator import admin_token_required
from ..util.dto import RoleDto
from flask_jwt_extended import jwt_required
from app.main.util.decorator import admin_token_required
api = RoleDto.api
_role = RoleDto.role

@api.route('/')
class RoleList(Resource):
    @api.doc('list_of_create_role')
    @api.marshal_list_with(_role, envelope='data')
    def get(self):
        """List all role users"""
        return get_all_role()

    @api.response(201, 'Role successfully created.')
    @api.doc('create a new role')
    @api.expect(_role, validate=True)
    def post(self):
        """Creates a new Role """
        data = request.json
        return create_role(data=data)