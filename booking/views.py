from datetime import datetime
from django.db.models import Q

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

# Create your views here.
from booking.forms import SearchForm, CustomUserCreationForm, BookingForm
from booking.models import Room, CustomUser, Booking

'''
    Флаги контекста
    search = True/False  - необходимо рендерить шаблон с секцией поиска свободных номеров или без
    main = True/False - если True - вывод списка полученных номеров идет на главную страницу
'''

# класс с данными от предыдущего поиска (чтобы подтягивать в форму при рендеринге результатов)
class SearchFormData():
    ci = ''
    co = ''
    ad = 0
    kid = 0
    result = False
    id = None

    @staticmethod
    def reset():
        SearchFormData.ci = ''
        SearchFormData.co = ''
        SearchFormData.ad = 0
        SearchFormData.kid = 0
        SearchFormData.result = False

# обработчик формы поиска свободных номеров
def searching_results(request):
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
        try:
            checkin = datetime.strptime(SearchFormData.ci, '%d.%m.%Y').date()
            checkout = datetime.strptime(SearchFormData.co, '%d.%m.%Y').date()
            capacity = int(SearchFormData.ad) + int(SearchFormData.kid)
        except:
            SearchFormData.reset()
            return None
        SearchFormData.result = True
        '''
        запросы в БД для вычисления списка номеров (поиск свободных номеров с учетом базы бронирований)
        '''
        # фильтруем номера (ищем которые можно - (обратное от нельзя))
        books_ex = Booking.objects.exclude(Q(checkout__lte=checkin, checkout__lt=checkout) |
                                        Q(checkin__gte=checkout, checkin__gt=checkin))
        # фильтруем номера по признаку вместимости
        rooms = Room.objects.exclude(id__in=books_ex.all().values('room_id')).filter(capacity__gte=capacity)

        return rooms
    else:
        # эта ветка на тот случай если форма поиска не валидируется браузером ()
        SearchFormData.reset()
        return None


def home(request):
    '''
        страница домашняя
    '''
    if request.method == 'POST' and 'search' in request.POST:
        context = {'room_list': searching_results(request), 'search': True, 'data':SearchFormData}
        return render(request, 'room_list.html', context)

    # room_list = Room.objects.order_by('price')
    room_list = Room.objects.order_by('category')[::2]
    SearchFormData.reset()
    return render(request, 'room_list.html', {'room_list': room_list, 'main':True})


def room_list(request):
    '''
        страница с "Обзорный список номеров" (либо целиком либо с результатами поиска)
    '''
    if request.method == 'POST' and 'search' in request.POST:
        context = {'room_list': searching_results(request), 'search': True, 'data': SearchFormData}
        return render(request, 'room_list.html', context)

    room_list = Room.objects.order_by('price')
    return render(request, 'room_list.html', {'room_list': room_list, 'search': True})


def booking(request):
    '''
        заглушка с "Бронирование"
    '''
    if request.method == 'POST' and 'search' in request.POST:
        context = {'room_list': searching_results(request), 'search': True, 'data': SearchFormData}
        return render(request, 'room_list.html', context)

    return render(request, 'booking.html', {'search': True, 'data': SearchFormData})


def create_book(request, pk):
    '''
        страница "Бронирование номера"
    '''
    room_list = [Room.objects.get(pk=pk)]
    errors = {}

    def check_book(booking):
        room = Booking.objects.filter(room=booking.room.pk)
        check = room.all().exclude(Q(checkout__lte=booking.checkin, checkout__lt=booking.checkout) |
                                    Q(checkin__gte=booking.checkout, checkin__gt=booking.checkin))
        # если нашлось пересечение, значит запишет ошибку
        if check:
            errors['book'] = True
        # если вместимость номера меньше запрашиваемой, значит запишет ошибку
        if booking.kids + booking.adults > booking.room.capacity:
            errors['capacity'] = True
        # если бронирование прошло проверку и нет ошибок то False иначе вернет словарь с ошибками
        return False if not errors else errors

    if request.method == 'POST' and 'search' in request.POST:
        context = {'room_list': searching_results(request), 'search': True, 'data': SearchFormData}
        return render(request, 'room_list.html', context)

    elif request.method == 'POST' and 'booking' in request.POST:
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = Room.objects.get(pk=pk)
            errors = check_book(booking)
            if errors == False:
                booking.save()
                return redirect('success')

        context = {'room_list': room_list, 'search': False, 'form':form, 'errors': errors}
        return render(request, 'booking.html', context)
        # return redirect('fail')

    context = {'room_list': room_list, 'search': True, 'data':SearchFormData}
    return render(request, 'booking.html', context)

def success(request):
    return render(request, 'success.html')

def fail(request):
    return render(request, 'fail.html')

def aboutus(request):
    '''
        страница с "О нас"
    '''
    return render(request, 'aboutus.html', {'search': False})


def amenities(request):
    '''
        страница "Сервис и удобства"
    '''
    return render(request, 'amenities.html', {'search': False})


def contact(request):
    '''
        страница "Контакты"
    '''
    return render(request, 'contact.html', {'search': False})


def mylogin(request):
    '''
        страница "Логин"
    '''
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile', user.pk)
        else: return render(request, 'login.html', {'access': 'denided'})
    return render(request, 'login.html', {'search': False, 'mode':'login'})


def mylogout(request):
    '''
        страница "Логаут"
    '''
    logout(request)
    return redirect('login')


def registr(request):
    '''
        страница "Регистрация"
    '''
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
            return render(request, 'login.html', {'search': False, 'mode':'registr', 'form': form})

    return render(request, 'login.html', {'search': False, 'mode':'registr'})


@login_required
def profile(request, pk):
    '''
        страница "Профиль гостя"
    '''
    return render(request, 'profile.html', {'search': False, 'access': 'success'})