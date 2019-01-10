import time
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import fields
from app.utils import send_result, parse_req, send_error, FieldString
from app.model import Channel, Strategy

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

    data, totals = Channel.get_channels(search, page, page_size)
    _data = []
    for item in data.items:
        item = item.json()
        _data.append(item)

    return_data = dict(
        rows=_data,
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
        '_id': fields.Number(),
        'name': FieldString(),
        'channel': FieldString(),
        'strategy': fields.Number(),
        'status': FieldString(),
    }

    try:
        json_data = parse_req(params)
        _id = json_data.get('_id')
        name = json_data.get('name')
        channel = json_data.get('channel')
        strategy = json_data.get('strategy')
        status = json_data.get('status')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    exist = Channel.find_by_id(_id)
    if not exist:
        return send_error(message='Khong tim thay channel')

    exist.name = name
    exist.channel = channel
    exist.strategy = strategy
    exist.status = status
    exist.save_to_db()

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
        'strategy': fields.Number(),
        'status': FieldString(),
    }

    try:
        json_data = parse_req(params)
        new_name = json_data.get('name').strip().lower()
        strategy = json_data.get('strategy')
        name = json_data.get('name')
        channel = json_data.get('channel')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    exist = Channel.find_exist(new_name)
    if exist:
        return send_error(message='Duplicate channel')

    channel = Channel(status='active', strategy=strategy,
                      reporting=True, count_success=0,
                      count_fail=0, name=name, channel=channel)
    channel.save_to_db()
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

    exist = Channel.find_by_id(_id)
    if not exist:
        return send_error(message='Không thể tìm thấy vui lòng thử lại.')

    exist.delete_from_db()
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
