import os
from jwt import decode
from flask import jsonify, request
from functools import wraps
from app.models.user_model import User
from logging import getLogger

logger = getLogger(__name__)

def token_admin_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
            if not token:
                logger.warn('a valid token is missing')
                return jsonify({'message': 'a valid token is missing'}), 401

            try:
                data = decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
                current_user = User.query.filter_by(email = data['email']).first()

            except Exception as e:
                logger.warn('Could not decode token : ' + str(e))
                return jsonify({'message': 'token is invalid'}), 401
            if current_user.isModerator:
                return f(current_user, *args, **kwargs)
            else:
                logger.warn('user is not admin')
                return jsonify({'message': 'user is not admin'}), 401
        return decorated