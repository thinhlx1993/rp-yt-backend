# coding=utf-8
from celery import Celery
from app.settings import *
from app.app import create_app

CONFIG = DevConfig if os.environ.get('FLASK_DEBUG') == '1' else ProdConfig


def make_celery(app):
    """
    Make celery task
    :param app:
    :return:
    """
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_BACKEND_URL'],
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app=create_app(CONFIG, 'celery'))
