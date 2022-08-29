from django.urls import path

from booking.views import home, booking, aboutus, amenities, contact, login, room_list

urlpatterns = [
    path('', home, name='home'),
    path('rooms/', room_list, name='rooms'),
    path('booking/', booking, name='booking'),
    path('aboutus/', aboutus, name='aboutus'),
    path('amenities/', amenities, name='amenities'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),

]