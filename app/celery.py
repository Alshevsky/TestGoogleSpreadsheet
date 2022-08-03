from __future__ import absolute_import, unicode_literals
import os
import redis
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app', backend='redis', broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.now = timezone.now

app.conf.beat_schedule = {
    'updating_exchange_rate': {
        'task': 'currency_converter.tasks.tasks.updating_exchange_rate',
        'schedule': crontab(hour='*/24'),
    },
    'table_parser': {
        'task': 'orders.tasks.tasks.table_parser',
        'schedule': crontab(hour='*/2'),
    },
}

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
