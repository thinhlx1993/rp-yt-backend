from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import fields
from app.utils import send_result, parse_req, send_error, FieldString
from app.model import Email
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

    data, totals = Email.find_by_keyword(keyword=search, page=page, page_size=page_size)
    emails = list()
    for item in data.items:
        emails.append(item.json())

    return_data = dict(
        rows=emails,
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
        'id': fields.Number,
        'email': FieldString(),
        'password': FieldString(),
        'recovery_email': FieldString(),
        'phone': FieldString(),
        'date': FieldString()
    }

    try:
        json_data = parse_req(params)
        email_id = json_data.get('id')
        password = json_data.get('password')
        email = json_data.get('email')
        recovery_email = json_data.get('recovery_email')
        date = json_data.get('date')
        phone = json_data.get('phone')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    email_obj = Email.find_by_id(email_id)
    if email_obj is None:
        return send_error(message='Not found email')

    email_obj.email = email
    email_obj.password = password
    email_obj.recovery_email = recovery_email
    email_obj.date = date
    email_obj.phone = phone
    email_obj.save_to_db()

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
        'date': FieldString(),
        'phone': FieldString()
    }

    try:
        json_data = parse_req(params)
        new_email = json_data.get('email').strip().lower()
        password = json_data.get('password')
        recovery_email = json_data.get('recovery_email')
        date = json_data.get('date')
        phone = json_data.get('phone')
    except Exception as ex:
        return send_error(message='Json parser error', code=442)

    email_obj = Email.find_by_email(email=new_email)
    if email_obj is not None:
        return send_error(message='Duplicate email')

    email_obj = Email(
        email=new_email,
        password=password,
        recovery_email=recovery_email,
        date=date,
        phone=phone,
        status=True,
    )
    email_obj.save_to_db()
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

    email = Email.find_by_id(_id)
    if email is None:
        return send_error(message='Không thể tìm thấy email, vui lòng thử lại.')

    email.delete_from_db()
    return send_result(message='Đã xóa thành công.')
