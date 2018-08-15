import time
import datetime
from flask import Blueprint, request
from bson import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity
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
    try:
        page = int(request.args.get('page'))
        page_size = int(request.args.get('size'))
        search = request.args.get('search', '')
    except Exception as ex:
        return send_error(message='Json parse error')

    query = dict()
    if search and search != '':
        query['username'] = {"$regex": search}

    data = client.db.user.find(query).skip(page_size * page).limit(page_size)
    totals = client.db.user.count({})
    data = list(data)
    for item in data:
        item['_id'] = str(item['_id'])
        del item['password']

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
        'role': FieldString(),
    }

    try:
        json_data = parse_req(params)
        _id = json_data.get('_id')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    user = client.db.user.find_one({'_id': ObjectId(_id)})
    if user is None:
        return send_error(message='Not found user')

    keys = ('address', 'phone', 'fullname', 'role')

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
        'role': FieldString(),
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

    keys = ('username', 'address', 'phone', 'fullname', 'role')

    user = dict()
    for k in keys:
        v = json_data.get(k, None)
        if v is not None or v != '':
            user[k] = v

    user['password'] = generate_password_hash(password)
    user['create_date'] = int(time.time())
    client.db.user.insert_one(user)
    return send_result(message='Create user successfully')


@api.route('', methods=['DELETE'])
def delete_user():
    """
    DELETE user
    :return:
    """

    try:
        _id = request.args.get('id', '')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    user = client.db.user.find_one({'_id': ObjectId(_id)})
    if user is None:
        return send_error(message='Không thể tìm thấy người dùng này, vui lòng thử lại.')

    if user['role'] != 'admin':
        return send_error(message='Bạn không thể xóa người dùng này!')

    if user['username'] == 'Administrator':
        return send_error(message='Không thể xóa người dùng này!')

    client.db.user.remove({'_id': ObjectId(_id)})
    return send_result(message='Đã xóa thành công.')


@api.route('password', methods=['PUT'])
@jwt_required
def update_password():
    """
    Update user password
    :return:
    """
    params = {
        '_id': FieldString(),
        'password': FieldString(),
    }

    try:
        json_data = parse_req(params)
        _id = json_data.get('_id')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    user = client.db.user.find_one({'_id': ObjectId(_id)})
    if user is None:
        return send_error(message='Không tìm thấy người dùng, tải lại trang.')

    if user['username'] != 'Administrator':
        return send_error(message='Bạn không thể đổi mật khẩu, chỉ admin mới có quyền đổi.')

    client.db.user.update({'_id': ObjectId(_id)}, user)
    return send_result(message='Thay đổi mật khẩu thành công.')


@api.route('/info', methods=['GET'])
@jwt_required
def get_user_info():
    """
    Get user info
    :return:
    """
    _id = get_jwt_identity()
    user = client.db.user.find_one({'_id': ObjectId(_id)})
    if user is None:
        return send_error(message='Không tìm thấy người dùng, tải lại trang.')
    return_data = dict(
        role=user['role'],
        username=user['username']
    )
    return send_result(data=return_data)
