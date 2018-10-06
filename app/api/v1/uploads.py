import pandas as pd
from flask import Blueprint, request
from app.utils import send_result, send_error
from app.model import Email
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

    keys = ('email', 'password', 'recovery_email', 'date', 'phone')
    new_email = 0
    error_email = 0
    for index, row in data_xls.iterrows():
        email = Email(
            email=row.get('email'),
            password=row.get('password'),
            recovery_email=row.get('recovery_email'),
            date=row.get('date'),
            phone=row.get('phone'),
            status=True
        )

        email_exist = Email.find_by_email(email.email)
        if not email_exist and email.email != '':
            new_email += 1
            email.save_to_db()
        else:
            error_email += 1

    return_data = dict(
        new_email=new_email,
        duplicated_email=error_email
    )
    return send_result(data=return_data, message='Upload file successfully')
