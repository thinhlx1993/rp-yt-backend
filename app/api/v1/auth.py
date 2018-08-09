import time
import string
import random

from bson import ObjectId
from datetime import timedelta
from marshmallow import fields

from flask import Blueprint, redirect, request
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
from app.extensions import jwt, redis_store, client, red
from app.utils import parse_req, FieldString, send_result, send_error
from app.task import send_email_verify as send_mail, send_email_forgot
from app.enums import *
from flask_jwt_extended import (
    jwt_required, create_access_token, jwt_refresh_token_required, get_jwt_identity, create_refresh_token,
    get_raw_jwt, get_jti
)


# image = ImageCaptcha(fonts=['app/template/fonts/Audiowide-Regular.ttf',
#                             'app/template/fonts/DancingScript-Regular.ttf'])

ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=1)
revoked_store = red


api = Blueprint('auth', __name__)


@api.route('/login', methods=['POST'])
def login():
    """
    :response: {"messages": "success"}
    """

    params = {
        'email': FieldString(),
        'password': FieldString(),
    }

    try:
        json_data = parse_req(params)
        password = json_data.get('password').strip()
        email = json_data.get('email').strip().lower()
    except Exception as ex:
        return send_error(message='json parser error', code=442)

    user = client.db.user.find_one({'email': email})
    if user:
        activate = user['activate']
        if activate == USER_DEACTIVATE:
            return send_error(data='user.deactivate',
                              message='Your account is deactivated, please contact administrator to activate')

        elif activate == USER_INACTIVATED:
            return send_error(data='user.notActivated',
                              message='An account has been prepared with this email address, but the email has not yet been confirmed. Please confirm your email.')

        elif activate == USER_ACTIVATED and check_password_hash(user['password'], password):
            access_token = create_access_token(identity=str(user['_id']), expires_delta=ACCESS_EXPIRES)
            refresh_token = create_refresh_token(identity=str(user['_id']), expires_delta=REFRESH_EXPIRES)
            access_jti = get_jti(encoded_token=access_token)
            refresh_jti = get_jti(encoded_token=refresh_token)
            revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
            revoked_store.set(refresh_jti, 'false', REFRESH_EXPIRES * 1.2)
            user_token = dict(
                _id=ObjectId(),
                user_id=user['_id'],
                access_jti=access_jti,
                refresh_jti=refresh_jti
            )
            client.db.token.insert_one(user_token)
            return send_result(data={'access_token': access_token, 'refresh_token': refresh_token, 'role': user['user_type']},
                               message='Successfully logged in to the Crypto Prediction')
        else:
            return send_error(message='Login failed. Wrong email or password')
    else:
        return send_error(message='Login failed. Wrong email or password')


@api.route('/register', methods=['POST'])
def register():
    """
    register user
    :response: {"messages": "success"}
    """

    params = {
        'name': FieldString(),
        'password': FieldString(),
        'address': FieldString(),
        'phone': FieldString(),
        'fullname': FieldString(),
        'email': fields.Email(),
    }

    try:
        json_data = parse_req(params)
        password = json_data.get('password').strip()
        email = json_data.get('email').strip().lower()
        fullname = json_data.get('fullname')
        address = json_data.get('address')
        phone = json_data.get('phone')
    except Exception as ex:
        return send_error(message='json parser error', code=442)

    user = client.db.user.find_one({'email': email})

    # reset password
    if user:
        activate = user['activate']
        if activate == USER_DEACTIVATE:
            return send_error(data='user.password',
                              message='Your account is deactivated, please contact administrator to activate')
        elif activate == USER_INACTIVATED:
            return send_error(data='user.notActivated',
                              message='An account has been prepared with this email address, but the email has not yet been confirmed. Please confirm your email.')

    if user is None:
        if 7 < len(password) < 50:
            password_hash = generate_password_hash(password)
            verify_code = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(40)])
            user_id = ObjectId()
            new_user = dict(
                _id=user_id,
                email=email,
                fullname=fullname,
                password=password_hash,
                address=address,
                phone=phone,
                created_date=int(time.time()),
                user_type='user',
                activate=USER_INACTIVATED,
                verify_code=verify_code,
                recovery_code=None,
                recovery_exp_date=None,
                sentiment=[],
                predict=[]
            )
            new_test_trade = dict(
                user_id=user_id,
                usd=5000,
                eth=0
            )
            client.db.user.insert_one(new_user)
            client.db.test_trade.insert_one(new_test_trade)
            send_mail.delay(email, verify_code)
            return send_result(message='Thank you for signing up. You will shortly receive an email confirming your registration. Please check the inbox of your email and confirm the registration.')
        else:
            return send_error(message='Your password must be at least 8 characters long')


@api.route('/verify/<string:email>/<string:verify_code>', methods=['GET'])
def verify_email(email, verify_code):
    """
    verify user email
    :response: {"messages": "success"}
    """
    # endpoint = 'http://localhost:4200'
    email = email.strip().lower()
    endpoint = 'https://crypto.stg.deu.boot.ai'
    user = client.db.user.find_one({'email': email})
    if user is not None:
        if user['activate'] == USER_ACTIVATED:
            return redirect(endpoint + '/#/login?status=true&message=Your account is activated')

        elif user['activate'] == USER_INACTIVATED and safe_str_cmp(verify_code, user['verify_code']):
            client.db.user.update_one({'_id': user['_id']}, {'$set': {'activate': USER_ACTIVATED, 'verify_code': None}})
            return redirect(endpoint + '/#/login?status=true&message=Your account has been activated')
        elif user['activate'] == USER_DEACTIVATE:
            return redirect(endpoint + '/#/login?status=false&message=Your account is deactivate, Please contact administrator!')

    return redirect(endpoint + '/#/login?status=false&message=We can not find your email or email is activated')


@api.route('/recover', methods=['POST'])
def recover():
    """
    recover password

    :response: {"messages": "success"}
    """

    params = {
        'email': fields.Email()
    }

    try:
        json_data = parse_req(params)
        email = json_data.get('email').strip().lower()
        # captcha_code = json_data.get('captcha')
    except Exception as ex:
        return send_error(message='Your email is incorrect')

    # address = request.remote_addr
    # old_captcha = redis_store.get(address).decode("utf-8")
    # captcha_code = captcha_code.lower()
    # if captcha_code == old_captcha:

    # update recovery date and code to database
    user = client.db.user.find_one({'email': email})
    if user is None:
        return send_result(message='The entered e-mail address is not yet registered or not verified!')

    # check user activate or deactivate
    activate = user['activate']
    if activate == USER_DEACTIVATE:
        return send_error(data='user.password',
                          message='Your email is deactivated, please contact administrator to activate')
    elif activate == USER_INACTIVATED:
        return send_error(data='user.notActivated',
                          message='An email has been prepared with this email address, but the email has not yet been confirmed. Please confirm your email.')

    if user['recovery_exp_date'] is not None:
        if int(user['recovery_exp_date']) > int(time.time()):
            return send_result(message='You already request change password, please check your mailbox')

    random_string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(40)])
    client.db.user.update_one({'_id': user['_id']}, {'$set': {'recovery_code': random_string,
                                                              'recovery_exp_date': int(time.time()) + (60 * 60 * 12)}})

    # after save all data of recovery, send mail to user
    send_email_forgot.delay(email, random_string)
    return send_result(message='You will shortly receive an email with a link. Please confirm that you want to change the password.')


@api.route('/reset', methods=['POST'])
def reset_password():
    """
    reset password

    :response: {"messages": "success"}
    """

    params = {
        'email': FieldString(),
        'password': FieldString(),
        'recovery_code': FieldString()
    }

    try:
        json_data = parse_req(params)
        email = json_data.get('email').strip().lower()
        password = json_data.get('password').strip()
        recovery_code = json_data.get('recovery_code')
    except Exception as ex:
        return send_error(message='json parser error', code=442)

    user = client.db.user.find_one({'email': email})

    if user is None:
        return send_error(message='Please check your email.')

    # check email expired
    if user['recovery_exp_date'] is not None:
        if int(user['recovery_exp_date']) < int(time.time()):
            return send_error(message='Invalid email or email has expired')

    # if email is valid time check password hash and recovery_code
    if user['recovery_code'] is not None and safe_str_cmp(user['recovery_code'], recovery_code):
        # if security code valid, change user password, clear security code
        if 50 > len(password) > 7:
            new_password = generate_password_hash(password)
            client.db.user.update_one({'_id': user['_id']},
                                      {'$set': {
                                          'password': new_password,
                                          'recovery_exp_date': None,
                                          'recovery_code': None}})
            # Revoker all token
            tokens = client.db.token.find({'user_id': user['_id']})
            tokens = list(tokens)
            for token in tokens:
                revoked_store.set(token['access_jti'], 'true', ACCESS_EXPIRES * 1.2)
                revoked_store.set(token['refresh_jti'], 'true', REFRESH_EXPIRES * 1.2)
            return send_result(message='Reset password success!')
        else:
            return send_error(message='Your password must be at least 8 characters long')
    else:
        return send_error(message='Your password Reset link has expired')
#
#
# @api.route('/captcha', methods=['GET'])
# def captcha():
#     """
#     get captcha code
#
#     :response: {"messages": "Captcha render success!", "data": "base64 code"}
#     """
#
#     # random string with 6 digit code a-z A-Z 0-9
#     # random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
#     random_string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
#     # random_string = '123456'
#     # generate captcha code
#     data = image.generate(random_string)
#     return_data = base64.b64encode(data.getvalue())
#     return_data = return_data.decode("utf-8")
#     return_data = "data:image/PNG;base64," + return_data
#     random_string = random_string.lower()
#     address = request.remote_addr
#     redis_store.set(address, random_string)
#     return send_result(data=str(return_data), message='Captcha render success!')


@api.route('/password', methods=['PUT'])
@jwt_required
def change_password():
    """
    :response: {"messages": "success"}
    """
    params = {
        'password': FieldString(),
        'newPassword': FieldString()
    }

    try:
        json_data = parse_req(params)
        password = json_data.get('password').strip()
        new_password = json_data.get('newPassword').strip()
        user_id = get_jwt_identity()
    except:
        return send_error(message='json parser error', code=442)

    user = client.db.user.find_one({'_id': ObjectId(user_id)})
    if user is None:
        return send_error(message='We can not found user', code=401)

    if check_password_hash(user['password'], password):
        if len(password) > 5:
            client.db.user.update_one({'_id': user['_id']}, {'$set': {'password': generate_password_hash(new_password)}})

            # Revoker all token
            tokens = client.db.token.find({'user_id': user['_id']})
            tokens = list(tokens)
            for token in tokens:
                revoked_store.set(token['access_jti'], 'true', ACCESS_EXPIRES * 1.2)
                revoked_store.set(token['refresh_jti'], 'true', REFRESH_EXPIRES * 1.2)
            return send_result(message='Password changed! Please login', code=401)
        else:
            return send_error(message='Password must be at least 6 characters long')
    else:
        return send_error(message='Wrong password, please recheck your password!', data='wrong-password')


# The jwt_refresh_token_required decorator insures a valid refresh
# token is present in the request before calling this endpoint. We
# can use the get_jwt_identity() function to get the identity of
# the refresh token, and use the create_access_token() function again
# to make a new access token for this identity.
@api.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    """
    Refresh token if token is expired
    :return:
    """
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    access_jti = get_jti(encoded_token=access_token)
    revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
    ret = {
        'access_token': access_token
    }
    return send_result(data=ret)


# Endpoint for revoking the current users access token
@api.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    """
    Add token to blacklist
    :return:
    """
    jti = get_raw_jwt()['jti']
    revoked_store.set(jti, 'true', ACCESS_EXPIRES * 1.2)

    # remove token from database
    client.db.token.remove({'access_jti': jti})

    return send_result(message='Successfully logged out')


# Endpoint for revoking the current users refresh token
@api.route('/logout2', methods=['DELETE'])
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()['jti']
    revoked_store.set(jti, 'true', REFRESH_EXPIRES * 1.2)
    return send_result(message='Successfully logged out')


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = revoked_store.get(jti)
    if entry is not None:
        entry = entry.decode("utf-8")
    if entry == 'false':
        return False
    return True
