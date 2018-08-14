import io
import csv
import time
import datetime
from flask import Blueprint, request
from bson import ObjectId
from flask_jwt_extended import jwt_required
from marshmallow import fields
from datetime import timedelta
from app.extensions import client
from werkzeug.security import generate_password_hash
from app.utils import send_result, parse_req, send_error, FieldString

ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=1)

api = Blueprint('uploads', __name__)


def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


@api.route('/email', methods=['POST'])
def upload_email():
    """
    Upload email as csv file and save to db
    :return:
    """
    f = request.files['file']
    if not f:
        return send_error(message='No file')

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    keys = ('email', 'password', 'recovery_email', 'date')
    new_email = 0
    duplicated_email = 0
    for row in csv_input:
        email = dict()
        for index, key in enumerate(keys):
            email[key] = row[index]

        email_exist = client.db.email.find_one({'email': email['email']})
        if not email_exist:
            new_email += 1
            client.db.email.insert_one(email)
        else:
            duplicated_email += 1

    return_data = dict(
        new_email=new_email,
        duplicated_email=duplicated_email
    )
    return send_result(data=return_data, message='Upload file successfully')
