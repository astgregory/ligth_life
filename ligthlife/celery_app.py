import os
import time

from django.core.mail import send_mail


from celery import Celery
#
from django.conf import settings



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ligthlife.settings')

app = Celery('ligthlife')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()




@app.task()
# def debug_task():
#     time.sleep(20)
#     print('Hello from debug_task')

def mail_send():
    send_mail('Погода',
              'Тестовое сообщение',
              'astgregory87@gmail.com',
              ['astgregory@bk.ru'])

# mail_send()
