# -*- coding: utf-8 -*-
import logging
import os
import traceback
from time import strftime
from flask import Flask, request

from app.api import v1 as api_v1
from app.extensions import jwt, client, app_log_handler, celery
from .settings import ProdConfig


def create_app(config_object=ProdConfig):
    """
    Init App
    :param config_object:
    :param name:
    :return:
    """
    app = Flask(__name__, static_url_path="", static_folder="./template", template_folder="./template")
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """
    Init extension
    :param app:
    :return:
    """
    client.app = app
    client.init_app(app)
    celery.init_app(app)
    jwt.init_app(app)
    if os.environ.get('FLASK_DEBUG') == '0':
        # logger
        logger = logging.getLogger('api')
        logger.setLevel(logging.ERROR)
        logger.addHandler(app_log_handler)

        @app.after_request
        def after_request(response):
            # This IF avoids the duplication of registry in the log,
            # since that 500 is already logged via @app.errorhandler.
            if response.status_code != 500:
                ts = strftime('[%Y-%b-%d %H:%M]')
                logger.error('%s %s %s %s %s %s',
                             ts,
                             request.remote_addr,
                             request.method,
                             request.scheme,
                             request.full_path,
                             response.status)
            return response

        @app.errorhandler(Exception)
        def exceptions(e):
            ts = strftime('[%Y-%b-%d %H:%M]')
            tb = traceback.format_exc()
            logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                         ts,
                         request.remote_addr,
                         request.method,
                         request.scheme,
                         request.full_path,
                         tb)
            return "Internal Server Error", 500


def register_blueprints(app):
    """
    Init blueprint for api url
    :param app:
    :return:
    """
    app.register_blueprint(api_v1.auth.api, url_prefix='/api/v1/auth')
    app.register_blueprint(api_v1.user.api, url_prefix='/api/v1/user')
    app.register_blueprint(api_v1.uploads.api, url_prefix='/api/v1/uploads')
    app.register_blueprint(api_v1.email.api, url_prefix='/api/v1/email')
    app.register_blueprint(api_v1.strategy.api, url_prefix='/api/v1/strategy')
    app.register_blueprint(api_v1.channel.api, url_prefix='/api/v1/channel')
