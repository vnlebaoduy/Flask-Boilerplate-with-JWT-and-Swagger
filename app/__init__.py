from flask_restplus import Api
from flask import Blueprint
from os import environ, path

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
          title=environ.get('APP_TITLE', 'REST API'),
          version=environ.get('APP_VERSION', '0.1'),
          description=environ.get('APP_DESCRIPTION', 'description API'),
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(role_ns, path='/role')
