from bson import ObjectId
from datetime import timedelta
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import jwt
from app.utils import parse_req, FieldString, send_result, send_error
from flask_jwt_extended import (
    jwt_required, create_access_token, jwt_refresh_token_required, get_jwt_identity, create_refresh_token,
    get_raw_jwt
)

from app.model import User

ACCESS_EXPIRES = timedelta(days=7)
REFRESH_EXPIRES = timedelta(days=30)


api = Blueprint('auth', __name__)
blacklist = set()


@api.route('/login', methods=['POST'])
def login():
    """
    :response: {"messages": "success"}
    """

    params = {
        'username': FieldString(),
        'password': FieldString(),
    }

    try:
        json_data = parse_req(params)
        password = json_data.get('password').strip()
        username = json_data.get('username').strip().lower()
    except Exception as ex:
        return send_error(message='json parser error', code=442)

    user = User.find_by_username(username=username)
    if user:
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id, expires_delta=ACCESS_EXPIRES)
            refresh_token = create_refresh_token(identity=user.id, expires_delta=REFRESH_EXPIRES)
            return send_result(data={'access_token': access_token,
                                     'refresh_token': refresh_token},
                               message='Successfully logged in to the Dashboard')
        else:
            return send_error(message='Login failed. Wrong username or password')
    else:
        return send_error(message='Login failed. Wrong username or password')


@api.route('/password', methods=['PUT'])
@jwt_required
def change_password():
    """
    :response: {"messages": "success"}
    """
    params = {
        'password': FieldString(),
        'newPassword': FieldString()
    }

    try:
        json_data = parse_req(params)
        password = json_data.get('password').strip()
        new_password = json_data.get('newPassword').strip()
        user_id = get_jwt_identity()
    except:
        return send_error(message='json parser error', code=442)

    user = User.find_by_id(user_id=user_id)
    if user is None:
        return send_error(message='We can not found user', code=401)

    if check_password_hash(user['password'], password):
        if len(password) > 5:
            user.password = generate_password_hash(new_password)
            user.save_to_db()
            return send_result(message='Password changed! Please login', code=401)
        else:
            return send_error(message='Password must be at least 6 characters long')
    else:
        return send_error(message='Wrong password, please recheck your password!', data='wrong-password')


# The jwt_refresh_token_required decorator insures a valid refresh
# token is present in the request before calling this endpoint. We
# can use the get_jwt_identity() function to get the identity of
# the refresh token, and use the create_access_token() function again
# to make a new access token for this identity.
@api.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    """
    Refresh token if token is expired
    :return:
    """
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    ret = {
        'access_token': access_token
    }
    return send_result(data=ret)


# Endpoint for revoking the current users access token
@api.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    """
    Add token to blacklist
    :return:
    """
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)

    return send_result(message='Successfully logged out')


# Endpoint for revoking the current users refresh token
@api.route('/logout2', methods=['DELETE'])
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return send_result(message='Successfully logged out')


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist
