from app.extensions import client
from app.task import send_email_forgot, send_email_price, send_email_verify


def resend():
    with client.app.app_context():
        emails = client.db.email_scheduler.find({'status': False, 'on_sending': False})
        for item in list(emails):
            mail_type = item['type']
            email = item['email']
            _id = str(item['_id'])
            if mail_type == 'send_email_verify':
                send_email_verify.delay(email, item['hash_password'], _id)

            elif mail_type == 'send_email_forgot':
                send_email_forgot.delay(email, item['security_question'], _id)

            elif mail_type == 'send_email_price':
                send_email_price.delay(email, item['fullname'], item['price'], _id)
