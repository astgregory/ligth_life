import os
import time

from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ligthlife.settings')

app = Celery('ligthlife')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.task()
def debug_task():
    time.sleep(10)
    print('Hello from debug task')



# from celery.schedules import crontab
#
# celery_app = Celery('tasks', broker='redis://localhost:6379/0')
#
# celery_app.conf.beat_schedule = {
#     'send_weather_report': {
#         'task': 'weather.tasks.send_weather_message',
#         'schedule': crontab(minute='*/1'),  # Запускать задачу каждую минуту (для тестирования)
#     },
# }
