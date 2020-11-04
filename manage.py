import os
import unittest
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app.main.model import user, role, permission, revoked_tokens
from app import blueprint
from flask_jwt_extended import JWTManager
from flask import jsonify
from app.main import create_app, db
from werkzeug.exceptions import HTTPException
from os import environ, path
from app.main.util.generator_sample_data import Seed
from dotenv import load_dotenv

# Loading Environment
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# Create App
app = create_app(environ.get('FLASK_ENV', 'development'))
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = environ.get(
    'JWT_SECRET_KEY', 'jwt-secret-string')
jwt = JWTManager(app)

# Config JWT & blueprint
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config.setdefault('RESTPLUS_MASK_SWAGGER', False)
app.register_blueprint(blueprint)
app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify({'status': 'fail', 'message': str(e)}), code


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return revoked_tokens.RevokedTokenModel.is_jti_blacklisted(jti)


@jwt.expired_token_loader
def my_expired_token_callback():
    return jsonify({
        'status': 'fail',
        'message': 'The token has expired'
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


@manager.command
def clear():
    try:
        db.session.query(role.Role).delete()
        db.session.query(user.User).delete()
        db.session.commit()
    except:
        db.session.rollback()


@manager.command
def seed():
    Seed.gen_role()
    Seed.gen_user()


if __name__ == '__main__':
    manager.run()
