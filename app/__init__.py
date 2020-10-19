from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.role_controller import api as role_ns

blueprint = Blueprint('api', __name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'jwt'
    }
}

api = Api(blueprint,
          authorizations=authorizations,
          title='HỆ THỐNG API ỨNG DỤNG CSGT C08',
          version='1.0 beta',
          description='Cung cấp các service phục vụ cho quản lý hệ thống tra cứu C08'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(role_ns, path='/role')