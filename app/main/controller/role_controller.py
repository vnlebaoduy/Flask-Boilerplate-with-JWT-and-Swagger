from flask import request
from flask_restplus import Resource, reqparse
from ..service.role_service import get_all_role, create_role, delete_role_id
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..util.dto import RoleDto

api = RoleDto.api
_role = RoleDto.role
_role_create = RoleDto.role_create


@api.route('/')
class RoleList(Resource):
    @api.doc('list_of_create_role')
    @api.response(204, 'Role is empty')
    @api.marshal_list_with(_role, envelope='data')
    @jwt_required
    def get(self):
        """List all role users"""
        roles = get_all_role()
        if not roles:
            return {'message': 'empty'}, 204
        else:
            return roles

    @api.response(201, 'Role successfully created.')
    @api.response(409, "Role already exists.")
    @api.doc('Creates a new Role')
    @jwt_required
    @api.expect(_role_create, validate=True)
    def post(self):
        """Creates a new Role """
        data = request.json
        return create_role(data=data)


@api.route('/<role_id>')
@api.doc('Delete a Role by id')
class DeleteRole(Resource):
    @api.param('role_id', 'The Role identifier')
    @api.response(200, 'Role successfully deleted.')
    @jwt_required
    def delete(self, role_id):
        """Delete a Role By id """
        return delete_role_id(role_id=role_id)
