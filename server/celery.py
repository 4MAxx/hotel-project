import os
from celery import Celery

from celery.schedules import crontab

from server.settings import CELERY_BROKER_URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {'tracing-expired-booking-every-day-at-00-05':
                            {
                            'task': 'booking.tasks.booking_expired_tracing_task',
                            'schedule': crontab(minute=0, hour='*/8'),
                            }
}

# app.conf.beat_schedule = {'send-notice-every-5-min':
#                             {
#                             'task': 'booking.tasks.send_email_task',
#                             'schedule': crontab(minute='*/1'),
#                             'args': ('mad_@tut.by',),
#                             }
# }