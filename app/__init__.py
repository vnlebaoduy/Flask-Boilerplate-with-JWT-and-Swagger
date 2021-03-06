from flask_restplus import Api
from flask import Blueprint
from os import environ
from .main.controller.user_controller import api as user_ns
from .main.controller.role_controller import api as role_ns
from .main.controller.permission_controller import api as permission_ns

blueprint = Blueprint('api', __name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    }
}

api = Api(blueprint,
          security = 'apikey',
          authorizations=authorizations,
          title=environ.get('APP_TITLE', 'REST API'),
          version=environ.get('APP_VERSION', '0.1'),
          description=environ.get('APP_DESCRIPTION', 'description API'),
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(role_ns, path='/role')
api.add_namespace(permission_ns, path='/permission')
