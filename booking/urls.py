from django.urls import path

from booking.views import home, booking, aboutus, amenities, contact, mylogin, room_list, registr, mylogout, profile

urlpatterns = [
    path('', home, name='home'),
    path('rooms/', room_list, name='rooms'),
    path('booking/', booking, name='booking'),
    path('aboutus/', aboutus, name='aboutus'),
    path('amenities/', amenities, name='amenities'),
    path('contact/', contact, name='contact'),
    path('login/', mylogin, name='login'),
    path('logout/', mylogout, name='logout'),
    path('registr/', registr, name='registr'),
    path('profile/<int:pk>/', profile, name='profile')

]