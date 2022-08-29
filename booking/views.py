from datetime import datetime

from django.shortcuts import render

# Create your views here.
from booking.forms import SearchForm
from booking.models import Room

def searching_rooms(request):
    # form = SearchForm(request.POST)
    # if form.is_valid():
    #     checkin = form.cleaned_data["checkin"]
    #     checkout = form.cleaned_data["checkout"]
    #     capacity = form.cleaned_data["adult"] + form.cleaned_data["kids"]
    ci = request.POST['checkin']
    co = request.POST['checkout']
    if ci and co:
        checkin = datetime.strptime(ci, '%m/%d/%Y').date()
        checkout = datetime.strptime(co, '%m/%d/%Y').date()
        capacity = int(request.POST['adults']) + int(request.POST['kids'])
        rooms_before = Room.objects.filter(checkout__lte=checkin, capacity__gte=capacity)
        rooms_after = Room.objects.filter(checkin__gte=checkout, capacity__gte=capacity)
        return rooms_after.union(rooms_before)
    else: return False


def home(request):
    if request.method == 'POST' and 'search' in request.POST:
        room_list = searching_rooms(request)
        if room_list:
            return render(request, 'room_list.html', {'room_list': room_list})
    room_list = Room.objects.all()
    return render(request, 'room_list_main.html', {'room_list': room_list})

def room_list(request):
    if request.method == 'POST' and 'search' in request.POST:
        room_list = searching_rooms(request)
        if room_list:
            return render(request, 'room_list.html', {'room_list': room_list})
    room_list = Room.objects.all()
    return render(request, 'room_list.html', {'room_list': room_list})


def booking(request):
    if request.method == 'POST' and 'search' in request.POST:
        room_list = searching_rooms(request)
        if room_list:
            return render(request, 'room_list.html', {'room_list': room_list})
    return render(request, 'booking.html')

def aboutus(request):
    return render(request, 'aboutus.html')

def amenities(request):
    return render(request, 'amenities.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    return render(request, 'login.html')