from datetime import datetime

from booking.models import Booking
from booking.service import send_email_signup_notice, send_booking_email, send_subj_mes_email
from server.celery import app

@app.task
def send_email_task(email):
    send_email_signup_notice(email)

@app.task
def send_booking_email_task(booking_id):
    send_booking_email(booking_id)

@app.task
def send_subj_mes_email_task(subject, message, email):
    send_subj_mes_email(subject, message, email)

@app.task
def booking_expired_tracing_task():
    books_ref = Booking.objects.filter(status_conf='2',
                                       deadline_conf__lt=datetime.today().date()).update(status_conf='4')

@app.task
def expire_notice_task():
    pass