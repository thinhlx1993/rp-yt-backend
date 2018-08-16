# coding=utf-8
import time
from app.extensions import celery, mail, client


@celery.task()
def print_hello():
    print('start')


@celery.task()
def stat_report():
    channel = client.db.channel.find_one({'status': 'active', 'reporting': False})
    if channel is not None:
        print(channel['name'])
        client.db.channel.update({'_id': channel['_id']}, {'$set': {'reporting': True}})
