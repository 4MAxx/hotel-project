from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from booking.models import Booking


def send_email_signup_notice(email):
    subject = 'Вы подписались на email рассылку'
    message = render_to_string('sign_for_email.html')
    to_email = email
    msg = EmailMessage(subject, message, to=[to_email])
    msg.send()

def send_booking_email(booking_id):
    booking = Booking.objects.get(pk=booking_id)
    subject = 'Новое бронирование в ГОСТИШКЕ'
    message = render_to_string('booking_email_notification.html', {'booking': booking,
                                                                   'name':booking.user.first_name})
    to_email = booking.user.email
    msg = EmailMessage(subject, message, to=[to_email])
    msg.send()

def send_subj_mes_email(subject, message, email):
    msg = EmailMessage(subject, message, to=[email])
    msg.send()