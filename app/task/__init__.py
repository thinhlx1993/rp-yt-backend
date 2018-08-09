# coding=utf-8
import os
import urllib.parse
import datetime
from bson import ObjectId
from flask_mail import Message
from pymongo import MongoClient
from app.extensions import celery, mail

app_domain = 'crypto.stg.deu.boot.ai'
app_port = '8003'
username = urllib.parse.quote_plus('root')
password = urllib.parse.quote_plus('1234567a@')
production_url = 'mongodb://%s:%s@27.72.147.222:27017/?connect=false' % (username, password)
uri = "mongodb://localhost:27017/?connect=false" \
    if os.environ.get('FLASK_DEBUG') == '1' else production_url
client = MongoClient(uri)


@celery.task()
def send_email_verify(email, hash_password, email_id=None):
    """
    Send email to verify user email
    :return:
    """
    if email_id is not None:
        client.crypto.email_scheduler.update_one({'_id': ObjectId(email_id)}, {'$set': {'on_sending': True}})

    msg = Message()
    msg.add_recipient(email)
    msg.subject = 'Crypto - EMail bestätigen'
    api_endpoint = 'https://' + app_domain + '/api/v1/auth/verify/' + email + '/' + hash_password
    msg.html = """
    <head></head>
        <body>
        <p>Welcome to Crypto Prediction. But first, let's finish setting up your account.</p>
        <p>Please confirm your email address by clicking on this link:</p>
        <a href=""" + api_endpoint + """ target="_blank">Email Adresse Best&aumltigen</a>
        <p>Cheers</p>
        <p>Your friends at Steemit</p>
        </body>
    """
    json = dict(
        email=email,
        hash_password=hash_password,
        send_date=datetime.datetime.utcnow(),
        type='send_email_verify'
    )
    try:
        mail.send(msg)
        if email_id is None:
            json['status'] = True
            client.crypto.email_scheduler.insert_one(json)
        else:
            client.crypto.email_scheduler.update_one({'_id': ObjectId(email_id)}, {'$set': {'status': True}})
    except Exception as ex:
        print(str(ex) + 'Resend mail: ' + email)
        if email_id is None:
            json['status'] = False
            json['on_sending'] = False
            client.crypto.email_scheduler.insert_one(json)
        if email_id is not None:
            client.crypto.email_scheduler.update_one({'_id': ObjectId(email_id)}, {'$set': {'on_sending': False}})


@celery.task()
def send_email_forgot(email, security_question, email_id=None):
    """
    Send email forget password for user
    :return:
    """
    if email_id is not None:
        client.crypto.email_scheduler.update_one({'_id': ObjectId(email_id)}, {'$set': {'on_sending': True}})

    msg = Message()
    msg.sender = "Crypto Prediction <crypto.prediction.ai@gmail.com>"
    msg.add_recipient(email)
    msg.subject = 'Crypto - Passwort zurücksetzen'
    # msg.body = "testing"
    api_endpoint = 'https://' + app_domain + '/#/recover-password?email='+email+'&security_code='+security_question+''
    msg.html = """<head></head>
        <body>
        <p>Hi my friend</p>
        <p>Click to link below to recover your password.</p>
        <a href=""" + api_endpoint + """ target="_blank">Password zur&uumlcksetzen</a>
        <p>Your friends at Crypto Prediction</p>
        </body>
    """
    json = dict(
        email=email,
        security_question=security_question,
        send_date=datetime.datetime.utcnow(),
        type='send_email_forgot'
    )
    try:
        mail.send(msg)
        if email_id is None:
            json['status'] = True
            client.crypto.email_scheduler.insert_one(json)
        else:
            client.crypto.email_scheduler.update_one({'_id': ObjectId(email_id)}, {'$set': {'status': True}})
    except Exception as ex:
        print(str(ex) + 'Resend mail: ' + email)
        if email_id is None:
            json['status'] = False
            json['on_sending'] = False
            client.crypto.email_scheduler.insert_one(json)
        if email_id is not None:
            client.crypto.email_scheduler.update_one({'_id': ObjectId(email_id)}, {'$set': {'on_sending': False}})


@celery.task()
def send_email_price(email, fullname, price, email_id=None):
    """
    Send email forget password for user
    :return:
    """
    if email_id is not None:
        client.crypto.email_scheduler.update_one({'_id': ObjectId(email_id)}, {'$set': {'on_sending': True}})

    msg = Message()
    msg.sender = "Crypto Prediction <crypto.prediction.ai@gmail.com>"
    msg.add_recipient(email)
    msg.subject = 'Crypto - Price Notification'
    # msg.body = "testing"
    msg.html = """<head></head>
        <body>
        <p>Hi """+fullname+"""</p>
        <p>Ethereum price has over """+str(price)+"""$</p>
        <p>Your friends at Crypto Prediction</p>
        </body>
    """
    json = dict(
        email=email,
        fullname=fullname,
        price=price,
        send_date=datetime.datetime.utcnow(),
        type='send_email_price'
    )
    try:
        mail.send(msg)
        if email_id is None:
            json['status'] = True
            client.crypto.email_scheduler.insert_one(json)
        else:
            client.crypto.email_scheduler.update_one({'_id': ObjectId(email_id)}, {'$set': {'status': True}})
    except Exception as ex:
        print(str(ex) + 'Resend mail: ' + email)
        if email_id is None:
            json['status'] = False
            json['on_sending'] = False
            client.crypto.email_scheduler.insert_one(json)
        if email_id is not None:
            client.crypto.email_scheduler.update_one({'_id': ObjectId(email_id)}, {'$set': {'on_sending': False}})
