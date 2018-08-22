#! bin/bash
celery worker -A app.celery --loglevel=INFO --pool=solo -f logs/celery_1.log
