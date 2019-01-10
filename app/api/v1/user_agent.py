import time
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import fields
from app.utils import send_result, parse_req, send_error, FieldString

api = Blueprint('user_agent', __name__)


@api.route('', methods=['GET'])
@jwt_required
def get_user_agent():
    """
    Using for get all data of user agent
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

    data = client.db.agents.find(query).skip(page_size * page).limit(page_size)
    totals = client.db.agents.count(query)
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
def update_user_agent():
    """
    Update user agent data
    :return:
    """
    params = {
        '_id': FieldString(),
        'name': FieldString(),
    }

    try:
        json_data = parse_req(params)
        _id = json_data.get('_id')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    agents = client.db.agents.find_one({'_id': ObjectId(_id)})
    if agents is None:
        return send_error(message='Not found')

    keys = ['name']

    for k in keys:
        v = json_data.get(k, None)
        if v is not None or v != '':
            agents[k] = v

    client.db.agents.update({'_id': ObjectId(_id)}, agents)
    return send_result(message='Cập nhật thành công.')


@api.route('', methods=['POST'])
def create_user_agent():
    """
    Create user agent
    :return:
    """
    params = {
        'name': FieldString(),
    }

    try:
        json_data = parse_req(params)
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    keys = ['name']

    agents = dict()
    for k in keys:
        v = json_data.get(k, None)
        if v is not None or v != '':
            agents[k] = v

    agents['create_date'] = int(time.time())
    client.db.agents.insert_one(agents)
    return send_result(message='Tạo mới thành công.')


@api.route('', methods=['DELETE'])
def delete_user_agent():
    """
    DELETE user agent
    :return:
    """

    try:
        _id = request.args.get('id', '')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    agents = client.db.agents.find_one({'_id': ObjectId(_id)})
    if agents is None:
        return send_error(message='Không thể tìm thấy vui lòng thử lại.')

    client.db.agents.remove({'_id': ObjectId(_id)})
    return send_result(message='Đã xóa thành công.')
