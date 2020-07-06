from functools import wraps
from flask import request
from flask_jwt_extended import get_jwt_identity
from app.main.model.user import User


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        username= get_jwt_identity()
        user = User.find_by_username(username)

        if not user:
            return { 'message':'User not found !'},404
        
        if not user.admin:
            return {
                'status': 'fail',
                'message': 'admin token required'
            }, 401
        return f(*args, **kwargs)

    return decorated