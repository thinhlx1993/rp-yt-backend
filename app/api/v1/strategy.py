import time
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import fields
from app.utils import send_result, parse_req, send_error, FieldString
from app.model import Strategy
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

    tmp, totals = Strategy.find_by_keyword(keyword=search, page=page, page_size=page_size)
    data = []
    for item in tmp.items:
        data.append(item.json())

    return_data = dict(
        rows=data,
        totals=totals
    )
    return send_result(data=return_data)


@api.route('/all', methods=['GET'])
@jwt_required
def get_strategies():
    """
    Using for get all data of emails
    :return:
    """
    tmp = Strategy.find_all()
    data = []
    for item in tmp.items:
        data.append(item.json*())

    return send_result(data=data)


@api.route('', methods=['PUT'])
@jwt_required
def update_strategy():
    """
    Update email data
    :return:
    """
    params = {
        'id': fields.Number(),
        'name': FieldString(),
        'issue': FieldString(),
        'sub_issue': FieldString(),
        'note': FieldString()
    }

    try:
        json_data = parse_req(params)
        strategy_id = json_data.get('id')
        name = json_data.get('name')
        issue = json_data.get('issue')
        sub_issue = json_data.get('sub_issue')
        note = json_data.get('note')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    strategy = Strategy.find_by_id(strategy_id=strategy_id)
    if strategy is None:
        return send_error(message='Not found')

    strategy.name = name
    strategy.issue = issue
    strategy.sub_issue = sub_issue
    strategy.note = note
    strategy.save_to_db()

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
        issue = json_data.get('issue')
        sub_issue = json_data.get('sub_issue')
        note = json_data.get('note')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    strategy = Strategy.find_by_name(name=new_name)
    if strategy is not None:
        return send_error(message='Duplicate strategy')

    strategy = Strategy(
        name=new_name,
        issue=issue,
        sub_issue=sub_issue,
        note=note,
        create_date=int(time.time())
    )
    strategy.save_to_db()
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

    strategy = Strategy.find_by_id(_id)
    if strategy is None:
        return send_error(message='Không thể tìm thấy chiến dịch, vui lòng thử lại.')

    strategy.delete_from_db()
    return send_result(message='Đã xóa thành công.')
