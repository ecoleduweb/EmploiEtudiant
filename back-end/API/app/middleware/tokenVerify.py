import os
from jwt import decode
from flask import jsonify, request
from functools import wraps
from app.models.user_model import User
from logging import getLogger

logger = getLogger(__name__)

def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
            if not token:
                logger.warning('No token provided')
                return jsonify({'message': 'a valid token is missing'}), 401

            try:
                data = decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
                current_user = User.query.filter_by(email = data['email']).first()

            except Exception as e:
                logger.warning('Could not decode token : ' + str(e))
                return jsonify({'message': 'token is invalid'}), 401
            return f(current_user, *args, **kwargs)
        return decorated