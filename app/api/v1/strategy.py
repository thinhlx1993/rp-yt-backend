import time
from flask import Blueprint, request
from bson import ObjectId
from flask_jwt_extended import jwt_required
from marshmallow import fields
from app.extensions import client
from app.utils import send_result, parse_req, send_error, FieldString

api = Blueprint('strategy', __name__)


@api.route('', methods=['GET'])
@jwt_required
def get_strategy():
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
        query['name'] = {"$regex": search}

    data = client.db.strategy.find(query).skip(page_size * page).limit(page_size)
    totals = client.db.strategy.count(query)
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
def update_strategy():
    """
    Update email data
    :return:
    """
    params = {
        '_id': FieldString(),
        'name': FieldString(),
        'issue': FieldString(),
        'sub_issue': FieldString(),
        'note': FieldString()
    }

    try:
        json_data = parse_req(params)
        _id = json_data.get('_id')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    strategy = client.db.strategy.find_one({'_id': ObjectId(_id)})
    if strategy is None:
        return send_error(message='Not found')

    keys = ('name', 'issue', 'sub_issue', 'note')

    for k in keys:
        v = json_data.get(k, None)
        if v is not None or v != '':
            strategy[k] = v

    client.db.strategy.update({'_id': ObjectId(_id)}, strategy)
    return send_result(message='Cập nhật chiến dịch thành công.')


@api.route('', methods=['POST'])
def create_strategy():
    """
    Create email
    :return:
    """
    params = {
        'name': FieldString(),
        'issue': FieldString(),
        'sub_issue': FieldString(),
        'note': FieldString()
    }

    try:
        json_data = parse_req(params)
        new_name = json_data.get('name').strip().lower()
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    strategy = client.db.strategy.find_one({'email': new_name})
    if strategy is not None:
        return send_error(message='Duplicate strategy')

    keys = ('name', 'issue', 'sub_issue', 'note')

    strategy = dict()
    for k in keys:
        v = json_data.get(k, None)
        if v is not None or v != '':
            strategy[k] = v

    strategy['create_date'] = int(time.time())
    client.db.strategy.insert_one(strategy)
    return send_result(message='Tạo chiến dịch thành công.')


@api.route('', methods=['DELETE'])
def delete_strategy():
    """
    DELETE email
    :return:
    """

    try:
        _id = request.args.get('id', '')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    strategy = client.db.strategy.find_one({'_id': ObjectId(_id)})
    if strategy is None:
        return send_error(message='Không thể tìm thấy chiến dịch, vui lòng thử lại.')

    client.db.strategy.remove({'_id': ObjectId(_id)})
    return send_result(message='Đã xóa thành công.')
