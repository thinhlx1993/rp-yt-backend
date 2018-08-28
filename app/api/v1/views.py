import time
from flask import Blueprint, request
from bson import ObjectId
from flask_jwt_extended import jwt_required
from marshmallow import fields
from app.extensions import client
from app.utils import send_result, parse_req, send_error, FieldString

api = Blueprint('views', __name__)


@api.route('', methods=['GET'])
@jwt_required
def get_keyword():
    """
    Using for get all data of views
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

    data = client.db.views.find(query).skip(page_size * page).limit(page_size)
    totals = client.db.views.count(query)
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
def update_keyword():
    """
    Update email data
    :return:
    """
    params = {
        '_id': FieldString(),
        'keyword': FieldString(),
        'channel': FieldString(),
        'status': FieldString(),
    }

    try:
        json_data = parse_req(params)
        _id = json_data.get('_id')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    views = client.db.views.find_one({'_id': ObjectId(_id)})
    if views is None:
        return send_error(message='Not found')

    keys = ('keyword', 'channel', 'status')

    for k in keys:
        v = json_data.get(k, None)
        if v is not None or v != '':
            views[k] = v

    client.db.views.update({'_id': ObjectId(_id)}, views)
    return send_result(message='Cập nhật kênh thành công.')


@api.route('', methods=['POST'])
def create_views():
    """
    Create email
    :return:
    """
    params = {
        'keyword': FieldString(),
        'channel': FieldString(),
        'status': FieldString(),
    }

    try:
        json_data = parse_req(params)
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    keys = ('keyword', 'channel', 'status')

    views = dict()
    for k in keys:
        v = json_data.get(k, None)
        if v is not None or v != '':
            views[k] = v

    views['create_date'] = int(time.time())
    views['count'] = 0
    client.db.views.insert_one(views)
    return send_result(message='Tạo kênh mới thành công.')


@api.route('', methods=['DELETE'])
def delete_views():
    """
    DELETE email
    :return:
    """

    try:
        _id = request.args.get('id', '')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    views = client.db.views.find_one({'_id': ObjectId(_id)})
    if views is None:
        return send_error(message='Không thể tìm thấy vui lòng thử lại.')

    client.db.views.remove({'_id': ObjectId(_id)})
    return send_result(message='Đã xóa thành công.')
