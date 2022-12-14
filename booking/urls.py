
from django.urls import path

from booking.views import home, booking, aboutus, amenities, contact, mylogin, room_list, registr, confirm_book, \
    cancel_book, confirm_email, activate, signup_for_email_success, payment_success, payment, payment_form
from booking.views import mylogout, profile, create_book, success, fail

urlpatterns = [
    path('', home, name='home'),
    path('rooms/', room_list, name='rooms'),
    path('booking/', booking, name='booking'),
    path('booking/create/<int:pk>/', create_book, name='create_book'),
    path('booking/confirmation/<int:pk>/', confirm_book, name='confirm_book'),
    path('booking/cancel/<int:pk>/', cancel_book, name='cancel_book'),
    path('confirmation/', confirm_email, name='confirm_email'),
    path('payment/<int:user_id>/<int:book_id>', payment, name='payment'),
    path('payment_form/<int:user_id>/<int:book_id>', payment_form, name='payment_form'),
    path('payment/success/', payment_success, name='payment_success'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('success/', success, name='success'),
    path('signup_success/', signup_for_email_success, name='signup_success'),
    path('fail/', fail, name='fail'),
    path('aboutus/', aboutus, name='aboutus'),
    path('amenities/', amenities, name='amenities'),
    path('contact/', contact, name='contact'),
    path('login/', mylogin, name='login'),
    path('logout/', mylogout, name='logout'),
    path('registr/', registr, name='registr'),
    path('profile/<int:pk>/', profile, name='profile')

]