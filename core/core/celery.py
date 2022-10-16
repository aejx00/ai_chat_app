import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'simulate_3s': {
        'task': 'chat.tasks.add',
        'schedule': 3.0
    }
}


app.autodiscover_tasks()