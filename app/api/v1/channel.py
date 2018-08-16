import time
from flask import Blueprint, request
from bson import ObjectId
from flask_jwt_extended import jwt_required
from marshmallow import fields
from celery.result import ResultBase
from app.extensions import client
from app.utils import send_result, parse_req, send_error, FieldString
from app.task import stat_report

api = Blueprint('channel', __name__)


@api.route('', methods=['GET'])
@jwt_required
def get_channel():
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

    data = client.db.channel.find(query).skip(page_size * page).limit(page_size)
    totals = client.db.channel.count(query)
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
def update_channel():
    """
    Update email data
    :return:
    """
    params = {
        '_id': FieldString(),
        'name': FieldString(),
        'channel': FieldString(),
    }

    try:
        json_data = parse_req(params)
        _id = json_data.get('_id')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    channel = client.db.channel.find_one({'_id': ObjectId(_id)})
    if channel is None:
        return send_error(message='Not found')

    keys = ('name', 'channel')

    for k in keys:
        v = json_data.get(k, None)
        if v is not None or v != '':
            channel[k] = v

    client.db.channel.update({'_id': ObjectId(_id)}, channel)
    return send_result(message='Cập nhật kênh thành công.')


@api.route('', methods=['POST'])
def create_channel():
    """
    Create email
    :return:
    """
    params = {
        'name': FieldString(),
        'channel': FieldString(),
    }

    try:
        json_data = parse_req(params)
        new_name = json_data.get('name').strip().lower()
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    channel = client.db.channel.find_one({'email': new_name})
    if channel is not None:
        return send_error(message='Duplicate channel')

    keys = ('name', 'channel')

    channel = dict()
    for k in keys:
        v = json_data.get(k, None)
        if v is not None or v != '':
            channel[k] = v

    channel['create_date'] = int(time.time())
    channel['status'] = 'active'
    channel['reporting'] = False
    client.db.channel.insert_one(channel)
    return send_result(message='Tạo kênh mới thành công.')


@api.route('', methods=['DELETE'])
def delete_channel():
    """
    DELETE email
    :return:
    """

    try:
        _id = request.args.get('id', '')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    channel = client.db.channel.find_one({'_id': ObjectId(_id)})
    if channel is None:
        return send_error(message='Không thể tìm thấy vui lòng thử lại.')

    client.db.channel.remove({'_id': ObjectId(_id)})
    return send_result(message='Đã xóa thành công.')


@api.route('/start', methods=['GET'])
def start_report():
    """
    Start report
    :return:
    """

    try:
        _id = request.args.get('id', '')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    channel = client.db.channel.find_one({'_id': ObjectId(_id)})
    if channel is None:
        return send_error(message='Không thể tìm thấy vui lòng thử lại.')

    start_report.delay()
    return send_result(message='Khởi tạo thành công')
