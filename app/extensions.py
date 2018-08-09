# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""
import os
from webargs.flaskparser import FlaskParser
from flask_celery import Celery
from flask_jwt_extended import JWTManager
from raven.contrib.flask import Sentry
from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_redis import FlaskRedis
from flask_apscheduler import APScheduler
from logging.handlers import RotatingFileHandler
from flask_socketio import SocketIO
import redis

parser = FlaskParser()
celery = Celery()
mail = Mail()
jwt = JWTManager()
client = PyMongo()
scheduler = APScheduler()
sentry = Sentry(dsn='https://199594b8eadd4921a419684b352502eb:af915ce916a041ba9d856ad0d7966fdb@sentry.io/1198489')
redis_store = FlaskRedis()
app_log_handler = RotatingFileHandler('logs/app.log', maxBytes=1000000, backupCount=30)
scheduler_log_handler = RotatingFileHandler('logs/scheduler.log', maxBytes=1000000, backupCount=30)
socketio = SocketIO()

if os.environ.get('FLASK_DEBUG') == '1':
    red = redis.StrictRedis(host='localhost')
else:
    red = redis.StrictRedis(host='160.44.205.82', password='1234567a@@')
