# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""
from webargs.flaskparser import FlaskParser
from flask_jwt_extended import JWTManager
from flask_celery import Celery
from flask_pymongo import PyMongo
from flask_mail import Mail
from logging.handlers import RotatingFileHandler

parser = FlaskParser()
jwt = JWTManager()
client = PyMongo()
app_log_handler = RotatingFileHandler('logs/app.log', maxBytes=1000000, backupCount=30)
celery = Celery()
mail = Mail()
