# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""
from webargs.flaskparser import FlaskParser
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_mail import Mail
from logging.handlers import RotatingFileHandler

parser = FlaskParser()
jwt = JWTManager()
app_log_handler = RotatingFileHandler('logs/app.log', maxBytes=1000000, backupCount=30)
mail = Mail()
db = SQLAlchemy()
client = PyMongo()
