from datetime import datetime

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

# Create your views here.
from booking.forms import SearchForm, CustomUserCreationForm
from booking.models import Room

# Флаги контекста
# search = True/False  - необходимо рендерить шаблон с секцией поиска свободных номеров или без

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
    if request.method == 'POST' and 'search' in request.POST:
        room_list = searching_rooms(request)
        if room_list != False:
            return render(request, 'room_list.html', {'room_list': room_list, 'search': True, 'data': SearchFormData})
    room_list = Room.objects.order_by('price')
    return render(request, 'room_list.html', {'room_list': room_list, 'search': True})

# вьюшка страницы "Бронирование"
def booking(request):
    if request.method == 'POST' and 'search' in request.POST:
        room_list = searching_rooms(request)
        if room_list != False:
            return render(request, 'room_list.html', {'room_list': room_list, 'search': True, 'data':SearchFormData})
    return render(request, 'booking.html', {'search': True})

# вьюшка страницы "О нас"
def aboutus(request):
    return render(request, 'aboutus.html', {'search': False})

# вьюшка страницы "Сервис и удобства"
def amenities(request):
    return render(request, 'amenities.html', {'search': False})

# вьюшка страницы "Контакты"
def contact(request):
    return render(request, 'contact.html', {'search': False})

# вьюшка страницы "Логин"
def mylogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile', user.pk)
        else: return render(request, 'login.html', {'access': 'denided'})
    return render(request, 'login.html', {'search': False, 'mode':'login'})

# вьюшка страницы "Логаут"
def mylogout(request):
    logout(request)
    return redirect('login')

# вьюшка страницы "Регистрация"
def registr(request):
    if request.method == 'POST' :
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user_group = Group.objects.get(name='Гость')
            user.groups.add(user_group)
            login(request, user)
            return redirect('profile', user.pk)
        else:
            print('not valid', form.errors)
            return render(request, 'login.html', {'search': False, 'mode':'registr', 'form': form})

    return render(request, 'login.html', {'search': False, 'mode':'registr'})

# вьюшка страницы "Профиль гостя"
@login_required
def profile(request, pk):
    return render(request, 'profile.html', {'search': False, 'access': 'success'})