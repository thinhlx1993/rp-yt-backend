import time
import datetime
from flask import Blueprint, request
from bson import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import fields
from datetime import timedelta
from werkzeug.security import generate_password_hash
from app.utils import send_result, parse_req, send_error, FieldString
from app.model import User

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

    data, totals = User.find_by_keyword(keyword=search, page=page, page_size=page_size)

    users = []
    for item in data.items:
        user = item.json()
        users.append(user)

    return_data = dict(
        rows=users,
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
        'id': fields.Number(),
        'address': FieldString(),
        'phone': FieldString(),
        'fullname': FieldString(),
        'role': FieldString(),
    }

    try:
        json_data = parse_req(params)
        _id = json_data.get('id')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    user = User.find_by_id(_id)
    if user is None:
        return send_error(message='Not found user')

    user.address = json_data.get('address', None)
    user.phone = json_data.get('phone', None)
    user.fullname = json_data.get('fullname', None)
    user.role = json_data.get('role', None)

    user.save_to_db()
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
        address = json_data.get('address')
        phone = json_data.get('phone')
        fullname = json_data.get('fullname')
        role = json_data.get('role')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    user = User.find_by_username(username)
    if user is not None:
        return send_error(message='Duplicate user')

    user = User(
        username=username,
        address=address,
        phone=phone,
        fullname=fullname,
        role=role,
        create_date=int(time.time()),
        password=generate_password_hash(password)
    )

    user.save_to_db()
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

    user = User.find_by_id(_id)
    if user is None:
        return send_error(message='Không thể tìm thấy người dùng này, vui lòng thử lại.')

    if user.role != 'admin':
        return send_error(message='Bạn không thể xóa người dùng này!')

    if user.role == 'Administrator':
        return send_error(message='Không thể xóa người dùng này!')

    user.delete_from_db()
    return send_result(message='Đã xóa thành công.')


@api.route('/password', methods=['PUT'])
@jwt_required
def update_password():
    """
    Update user password
    :return:
    """
    params = {
        'id': fields.Number(),
        'password': FieldString(),
    }

    try:
        json_data = parse_req(params)
        _id = json_data.get('id')
        password = json_data.get('password')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    user = User.find_by_id(_id)
    if user is None:
        return send_error(message='Không tìm thấy người dùng, tải lại trang.')

    if user.username != 'Administrator':
        return send_error(message='Bạn không thể đổi mật khẩu, chỉ admin mới có quyền đổi.')

    user.password = generate_password_hash(password)
    user.save_to_db()
    return send_result(message='Thay đổi mật khẩu thành công.')


@api.route('/info', methods=['GET'])
@jwt_required
def get_user_info():
    """
    Get user info
    :return:
    """
    _id = get_jwt_identity()
    user = User.find_by_id(_id)
    if user is None:
        return send_error(message='Không tìm thấy người dùng, tải lại trang.')
    return_data = dict(
        role=user.role,
        username=user.username
    )
    return send_result(data=return_data)
