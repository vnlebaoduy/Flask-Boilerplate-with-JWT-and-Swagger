import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app.main.model import user,revoked_tokens
from app import blueprint
from flask_jwt_extended import JWTManager,get_jwt_claims,verify_jwt_in_request
from flask import jsonify
from app.main import create_app, db

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config.setdefault('RESTPLUS_MASK_SWAGGER', False)
app.register_blueprint(blueprint)
app.app_context().push()


manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return revoked_tokens.RevokedTokenModel.is_jti_blacklisted(jti)


@jwt.expired_token_loader
def my_expired_token_callback():
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'message': 'Token đã hết hạn'
    }), 401


@manager.command
def run():
    app.run()

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()