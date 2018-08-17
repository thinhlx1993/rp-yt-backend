import time
from flask import Blueprint, request
from bson import ObjectId
from flask_jwt_extended import jwt_required
from marshmallow import fields
from datetime import timedelta
from app.extensions import client
from app.utils import send_result, parse_req, send_error, FieldString

api = Blueprint('email', __name__)


@api.route('', methods=['GET'])
@jwt_required
def get_emails():
    """
    Using for get all data of emails
    :return:
    """
    try:
        page = int(request.args.get('page', 0))
        page_size = int(request.args.get('size', 10))
        search = request.args.get('search', '')
    except Exception as ex:
        return send_error(message='Parser params error')
    query = dict()
    if search and search != '':
        query['email'] = {"$regex": search}

    data = client.db.email.find(query).skip(page_size * page).limit(page_size)
    totals = client.db.email.count(query)
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
def update_email():
    """
    Update email data
    :return:
    """
    params = {
        '_id': FieldString(),
        'email': FieldString(),
        'password': FieldString(),
        'recovery_email': FieldString(),
        'date': FieldString()
    }

    try:
        json_data = parse_req(params)
        _id = json_data.get('_id')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    email = client.db.email.find_one({'_id': ObjectId(_id)})
    if email is None:
        return send_error(message='Not found email')

    keys = ('email', 'password', 'recovery_email', 'date')

    for k in keys:
        v = json_data.get(k, None)
        if v is not None or v != '':
            email[k] = v

    client.db.email.update({'_id': ObjectId(_id)}, email)
    return send_result(message='Update email successfully')


@api.route('', methods=['POST'])
def create_email():
    """
    Create email
    :return:
    """
    params = {
        'email': fields.Email(),
        'password': FieldString(),
        'recovery_email': fields.Email(),
        'date': FieldString()
    }

    try:
        json_data = parse_req(params)
        new_email = json_data.get('email').strip().lower()
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    email = client.db.email.find_one({'email': new_email})
    if email is not None:
        return send_error(message='Duplicate email')

    keys = ('email', 'password', 'recovery_email', 'date')

    email = dict()
    for k in keys:
        v = json_data.get(k, None)
        if v is not None or v != '':
            email[k] = v

    email['create_date'] = int(time.time())
    email['status'] = True
    client.db.email.insert_one(email)
    return send_result(message='Create email successfully')


@api.route('', methods=['DELETE'])
def delete_email():
    """
    DELETE email
    :return:
    """

    try:
        _id = request.args.get('id', '')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    email = client.db.email.find_one({'_id': ObjectId(_id)})
    if email is None:
        return send_error(message='Không thể tìm thấy email, vui lòng thử lại.')

    client.db.email.remove({'_id': ObjectId(_id)})
    return send_result(message='Đã xóa thành công.')
