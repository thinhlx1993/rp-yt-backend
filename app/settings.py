# -*- coding: utf-8 -*-
import os
os_env = os.environ


class Config(object):
    SECRET_KEY = '3nF3Rn0'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class ProdConfig(Config):
    """Production configuration."""
    # app config
    ENV = 'prod'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    HOST = '0.0.0.0'
    TEMPLATES_AUTO_RELOAD = False
    # JWT Config
    JWT_SECRET_KEY = '1234567a@@'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    # MongoDB config
    MONGO_DBNAME = 'youtube'
    MONGO_HOST = '27.72.147.222'
    MONGO_USERNAME = 'root'
    MONGO_PASSWORD = '1234567a@'
    MONGO_AUTH_SOURCE = 'admin'
    MONGO_CONNECT = False
    CONNECT = False


class DevConfig(Config):
    """Development configuration."""
    # app config
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_ENABLED = True  # Disable Debug toolbar
    TEMPLATES_AUTO_RELOAD = True
    HOST = '0.0.0.0'
    # JWT Config
    JWT_SECRET_KEY = '1234567a@@'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    # MongoDB config
    MONGO_DBNAME = 'test-yt'
    MONGO_HOST = '27.72.147.222'
    MONGO_USERNAME = 'root'
    MONGO_PASSWORD = '1234567a@'
    MONGO_AUTH_SOURCE = 'admin'
    MONGO_CONNECT = False
    CONNECT = False
