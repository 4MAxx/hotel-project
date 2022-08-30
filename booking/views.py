from datetime import datetime

from django.shortcuts import render

# Create your views here.
from booking.forms import SearchForm
from booking.models import Room

# класс с данными от предыдущего поиска (чтобы подтягивать в форму при рендеринге результатов)
class SearchFormData():
    ci = ''
    co = ''
    ad = 0
    kid = 0
    result = False

# обработчик формы поиска свободных номеров
def searching_rooms(request):
    # form = SearchForm(request.POST)
    # if form.is_valid():
    #     checkin = form.cleaned_data["checkin"]
    #     checkout = form.cleaned_data["checkout"]
    #     capacity = form.cleaned_data["adult"] + form.cleaned_data["kids"]
    SearchFormData.ci = request.POST['checkin']
    SearchFormData.co = request.POST['checkout']
    SearchFormData.ad = request.POST['adults']
    SearchFormData.kid = request.POST['kids']
    if SearchFormData.ci and SearchFormData.co and SearchFormData.ad:
        SearchFormData.result = True
        checkin = datetime.strptime(SearchFormData.ci, '%m/%d/%Y').date()
        checkout = datetime.strptime(SearchFormData.co, '%m/%d/%Y').date()
        capacity = int(SearchFormData.ad) + int(SearchFormData.kid)

        # запросы в БД для вычисления непересекающихся дат (поиск свободныз номеров)
        rooms_before = Room.objects.filter(checkout__lte=checkin, capacity__gte=capacity)
        rooms_after = Room.objects.filter(checkin__gte=checkout, capacity__gte=capacity)
        return rooms_after.union(rooms_before).order_by('price')
    else:
        SearchFormData.result = False
        return False

# вьюшка домашней страницы
def home(request):
    if request.method == 'POST' and 'search' in request.POST:
        room_list = searching_rooms(request)
        if room_list != False:
            return render(request, 'room_list.html', {'room_list': room_list, 'search': True, 'data':SearchFormData})
    # room_list = Room.objects.order_by('price')
    room_list = Room.objects.order_by('category')[::2]
    return render(request, 'room_list_main.html', {'room_list': room_list})

# вьюшка страницы с "Обзорный список номеров" (либо целиком либо с результатами поиска)
def room_list(request):
    # search = True       флаг - необходимо рендерить с секцией поиска свободных номеров
    if request.method == 'POST' and 'search' in request.POST:
        room_list = searching_rooms(request)
        if room_list != False:
            return render(request, 'room_list.html', {'room_list': room_list, 'search': True, 'data': SearchFormData})
    room_list = Room.objects.order_by('price')
    return render(request, 'room_list.html', {'room_list': room_list, 'search': True})

# вьюшка страницы "Бронирование"
def booking(request):
    # search = True  # флаг - необходимо рендерить с секцией поиска свободных номеров
    if request.method == 'POST' and 'search' in request.POST:
        room_list = searching_rooms(request)
        if room_list != False:
            return render(request, 'room_list.html', {'room_list': room_list, 'search': True, 'data':SearchFormData})
    return render(request, 'booking.html', {'search': True})

# вьюшка страницы "О нас"
def aboutus(request):
    # search = False       # флаг - необходимо рендерить без секции поиска свободных номеров
    return render(request, 'aboutus.html', {'search': False})

# вьюшка страницы "Сервис и удобства"
def amenities(request):
    # search = False       # флаг - необходимо рендерить без секции поиска свободных номеров
    return render(request, 'amenities.html', {'search': False})

# вьюшка страницы "Контакты"
def contact(request):
    # search = False       # флаг - необходимо рендерить без секции поиска свободных номеров
    return render(request, 'contact.html', {'search': False})

# вьюшка страницы "Логин"
def login(request):
    # search = False       # флаг - необходимо рендерить без секции поиска свободных номеров
    return render(request, 'login.html', {'search': False})