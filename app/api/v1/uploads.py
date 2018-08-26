import pandas as pd
from flask import Blueprint, request
from app.extensions import client
from app.utils import send_result, send_error

api = Blueprint('uploads', __name__)


@api.route('/email', methods=['POST'])
def upload_email():
    """
    Upload email as csv file and save to db
    :return:
    """
    f = request.files['file']
    if not f:
        return send_error(message='No file')

    csv_input = list()
    try:
        data_xls = pd.read_excel(f)
        # stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        # csv_input = csv.reader(stream)
    except Exception as ex:
        return send_error(message=str(ex))

    keys = ('email', 'password', 'recovery_email', 'date')
    new_email = 0
    error_email = 0
    for index, row in data_xls.iterrows():
        email = dict(
            email='',
            password='',
            recovery_email='',
            date=''
        )
        for key_index, key in enumerate(keys):
            if key in row.keys():
                email[key] = row[key]

        email_exist = client.db.email.find_one({'email': email['email']})
        if not email_exist and email['email'] != '':
            new_email += 1
            email['status'] = True
            client.db.email.insert_one(email)
        else:
            error_email += 1

    return_data = dict(
        new_email=new_email,
        duplicated_email=error_email
    )
    return send_result(data=return_data, message='Upload file successfully')
