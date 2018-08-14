import time
import datetime
from flask import Blueprint, request
from bson import ObjectId
from flask_jwt_extended import jwt_required
from marshmallow import fields
from datetime import timedelta
from app.extensions import client
from werkzeug.security import generate_password_hash
from app.utils import send_result, parse_req, send_error, FieldString

ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=1)

api = Blueprint('user', __name__)


@api.route('', methods=['GET'])
@jwt_required
def get_users():
    """
    Using for get all data of user
    :return:
    """
    page = int(request.args.get('page'))
    page_size = int(request.args.get('size'))
    data = client.db.user.find({}).skip(page_size * page).limit(page_size)
    totals = client.db.user.count({})
    data = list(data)
    for item in data:
        item['_id'] = str(item['_id'])

    return_data = dict(
        rows=data,
        totals=totals
    )
    return send_result(data=return_data)


@api.route('', methods=['PUT'])
@jwt_required
def update_user():
    """
    Update user data
    :return:
    """
    params = {
        '_id': FieldString(),
        'address': FieldString(),
        'phone': FieldString(),
        'fullname': FieldString(),
    }

    try:
        json_data = parse_req(params)
        _id = json_data.get('_id')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    user = client.db.user.find_one({'_id': ObjectId(_id)})
    if user is None:
        return send_error(message='Not found user')

    keys = ('address', 'phone', 'fullname')

    for k in keys:
        v = json_data.get(k, None)
        if v is not None or v != '':
            user[k] = v

    client.db.user.update({'_id': ObjectId(_id)}, user)
    return send_result(message='Update user successfully')


@api.route('', methods=['POST'])
def create_user():
    """
    Create user
    :return:
    """
    params = {
        'username': FieldString(),
        'password': FieldString(),
        'address': FieldString(),
        'phone': FieldString(),
        'fullname': FieldString(),
    }

    try:
        json_data = parse_req(params)
        username = json_data.get('username').strip().lower()
        password = json_data.get('password').strip()
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    user = client.db.user.find_one({'username': username})
    if user is not None:
        return send_error(message='Duplicate user')

    keys = ('username', 'address', 'phone', 'fullname')

    user = dict()
    for k in keys:
        v = json_data.get(k, None)
        if v is not None or v != '':
            user[k] = v

    user['password'] = generate_password_hash(password)
    user['create_date'] = int(time.time())
    client.db.user.insert_one(user)
    return send_result(message='Create user successfully')
