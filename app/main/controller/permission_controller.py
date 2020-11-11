from flask import request
from flask_restplus import Resource
from ..service.permission_service import get_all_permission, create_permission, delete_permission_id, \
    update_permission_by_id, get_permission_by_id
from flask_jwt_extended import jwt_required
from ..util.dto import PermissionDto

api = PermissionDto.api
_permission = PermissionDto.permission
_permission_create = PermissionDto.permission_create


@api.route('/')
class PermissionList(Resource):
    @api.doc('list_of_create_permission')
    @api.response(204, 'Permission is empty')
    # @api.marshal_list_with(_permission, envelope='data')
    @jwt_required
    def get(self):
        """List all Permission """
        permissions = get_all_permission()
        if not permissions:
            return {'message': 'empty'}, 204
        else:
            return permissions

    @api.response(201, 'Permission successfully created.')
    @api.response(409, "Permission already exists.")
    @api.doc('Creates a new Permission')
    @jwt_required
    @api.expect(_permission_create, validate=True)
    def post(self):
        """Creates a new Permission """
        data = request.json
        return create_permission(data=data)


@api.route('/<permission_id>')
@api.doc('Delete a Permission by id')
class DeletePermission(Resource):
    @api.param('permission_id', 'The Permission identifier')
    @api.response(200, 'Permission successfully deleted.')
    @jwt_required
    def delete(self, permission_id):
        """Delete a Permission By id """
        return delete_permission_id(permission_id=permission_id)


@api.route('/get_permission_by_user_id/<public_id>')
@api.doc('Get Permission')
class GetPermissionUserById(Resource):
    @api.param('public_id', 'The User identifier')
    @api.response(200, 'OK')
    @jwt_required
    def get(self, public_id):
        """Get Permission User By Id"""
        return get_permission_by_id(public_id)


# @api.route('/set_permission/<permission_id>')
# @api.doc('set permission')
# class SetPermission(Resource):
#     @api.param('permission_id', 'Permission identifier')
#     @api.response(201, 'Permission successfully set.')
#     @jwt_required
#     def post(self, user_id):
#         """Set Permission By id """
#         data = request.json
#         res = set_permission_user_by_ids(data['permission_id'], user_id)
#         return res


@api.route('/update_permission')
@api.doc('set Permission')
class SetPermission(Resource):
    @api.param('id', 'Permission identifier')
    @api.param('name', 'Name')
    @api.param('description', 'Description')
    @api.response(200, 'Permission successfully set.')
    @jwt_required
    def put(self):
        """Set Permission By id """
        data = request.json
        res = update_permission_by_id(data)
        return res
