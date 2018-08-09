import datetime

from flask import Blueprint, request
from bson import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import fields
from datetime import timedelta

from app.extensions import client, red
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
    data = client.db.user.find(
        {},
        {'email': 1, 'fullname': 1, 'address': 1, 'phone': 1,
         'created_date': 1, 'user_type': 1, 'activate': 1}). \
        sort([('user_type', 1)]). \
        skip(page_size * page).limit(page_size)
    totals = client.db.user.count({})
    data = list(data)
    for item in data:
        item['_id'] = str(item['_id'])

    return_data = dict(
        rows=data,
        totals=totals
    )
    return send_result(data=return_data)


@api.route('/settings', methods=['GET'])
@jwt_required
def get_settings():
    """
    Get settings of user, use in setting page
    :return:
    """
    coin = request.args.get('coin')
    user_id = get_jwt_identity()
    user = client.db.user.find_one({'_id': ObjectId(user_id)})
    account = dict(
        email=user['email'],
        fullname=user['fullname'],
        address=user['address'],
        phone=user['phone'],
        created_date=user['created_date'],
    )

    settings = client.db.trade.find_one({'user_id': user_id, 'coin': coin})
    setting = dict()
    if settings:
        setting = dict(
            coin=coin,
            time_step=settings['time_step'],
            total_budget=settings['total_budget'],
            buy_method=settings['buy_method'],
            stop_loss=settings['stop_loss'],
            budget_per_transaction=settings['budget_per_transaction'],
            api_key=settings['api_key'],
            secret_key=settings['secret_key'],
            enable_trade=settings['enable_trade']
        )

    subscriber = client.db.subscriber.find_one({'user_id': user_id})
    subscribe=dict()
    if subscriber:
        subscribe = dict(
            auto_trade=subscriber['auto_trade'],
            price=subscriber['price'],
            threshold=subscriber['threshold'],
        )
    return_data = dict(
        account=account,
        setting=setting,
        subscriber=subscribe
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
        'user_type': FieldString(),
        'activate': FieldString(),
    }

    try:
        json_data = parse_req(params)
        _id = json_data.get('_id')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    user = client.db.user.find_one({'_id': ObjectId(_id)})
    if user is None:
        return send_error(message='Not found user')

    keys = ('address', 'phone', 'fullname', 'user_type', 'activate')

    for k in keys:
        v = json_data.get(k, None)
        if v is not None or v != '':
            user[k] = v

    client.db.user.update({'_id': ObjectId(_id)}, user)
    # Revoker all token
    tokens = client.db.token.find({'user_id': user['_id']})
    for token in list(tokens):
        red.set(token['access_jti'], 'true', ACCESS_EXPIRES * 1.2)
        red.set(token['refresh_jti'], 'true', REFRESH_EXPIRES * 1.2)

    return send_result(message='Update user successfully')
