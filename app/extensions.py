# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""
from webargs.flaskparser import FlaskParser
from flask_jwt_extended import JWTManager
from raven.contrib.flask import Sentry
from flask_pymongo import PyMongo
from logging.handlers import RotatingFileHandler

parser = FlaskParser()
jwt = JWTManager()
client = PyMongo()
sentry = Sentry(dsn='https://199594b8eadd4921a419684b352502eb:af915ce916a041ba9d856ad0d7966fdb@sentry.io/1198489')
app_log_handler = RotatingFileHandler('logs/app.log', maxBytes=1000000, backupCount=30)
