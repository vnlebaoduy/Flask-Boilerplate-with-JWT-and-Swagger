import uuid
import datetime

from app.main import db
from app.main.model.user import User

from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

JWT_REFRESH_TOKEN_EXPIRES = 15552000  # seconds
JWT_ACCESS_TOKEN_EXPIRES = 600 

def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def user_login(username, password):
    current_user = User.find_by_username(username)
    if not current_user:
        return {'message': 'User {} doesn\'t exist'.format(username)}

    if current_user and current_user.check_password(password):
        expiresAccesToken = datetime.timedelta(
            seconds=JWT_ACCESS_TOKEN_EXPIRES)
        expiresRefreshToken = datetime.timedelta(
            seconds=JWT_REFRESH_TOKEN_EXPIRES)
        access_token = create_access_token(
            identity=username, expires_delta=expiresAccesToken)
        refresh_token = create_refresh_token(
            identity=username, expires_delta=expiresRefreshToken)
        return {
            'message': 'Logged in as {}'.format(current_user.username),
            'username': current_user.username,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires': JWT_ACCESS_TOKEN_EXPIRES,
        }
    else:
        return {'message': 'Wrong credentials'}, 403
