from datetime import datetime

import braintree
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from booking.forms import SearchForm, CustomUserCreationForm, BookingForm, UploadAvatar, SignForEmailForm
from booking.models import Room, CustomUser, Booking
from booking.tokens import account_activation_token
from booking.tasks import send_email_task, send_booking_email_task, send_subj_mes_email_task
from server import settings
from server.settings import DISCOUNT_COST

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
    nights = 1
    nights_d = 1
    result = False
    id = None
    error_date = False

    @staticmethod
    def reset():
        SearchFormData.ci = ''
        SearchFormData.co = ''
        SearchFormData.ad = 0
        SearchFormData.kid = 0
        SearchFormData.nights = 1
        SearchFormData.nights_d = 1
        SearchFormData.result = False
        SearchFormData.error_date = False


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
    SearchFormData.error_date = False

    if SearchFormData.ci and SearchFormData.co and SearchFormData.ad:
        try:
            checkin = datetime.strptime(SearchFormData.ci, '%d.%m.%Y').date()
            checkout = datetime.strptime(SearchFormData.co, '%d.%m.%Y').date()
            if checkin < checkout:
                SearchFormData.nights = (checkout - checkin).days
                # расчет дисконта (применяется для vip-гостя)
                SearchFormData.nights_d = float(SearchFormData.nights / 100 * (100 - DISCOUNT_COST))
            else:
                # если пользователь ввел дату заезда более позднюю чем дату выезда или "==", то нужно выводить ошибку
                SearchFormData.result = True
                SearchFormData.error_date = True
                return None

            capacity = int(SearchFormData.ad) + int(SearchFormData.kid)
        except:
            SearchFormData.reset()
            return None
        SearchFormData.result = True
        '''
        запросы в БД для вычисления списка номеров (поиск свободных номеров с учетом базы бронирований)
        '''

        # фильтруем номера (ищем которые нельзя)
        books_ex = Booking.objects.exclude(
            Q(checkout__lte=checkin, checkout__lt=checkout) | Q(checkin__gte=checkout, checkin__gt=checkin))
        # оставляем только подтвержденные или в стадии подтверждения
        books_ex2 =books_ex.filter(status_conf__in=['1','2'])

        # фильтруем номера по признаку вместимости (исключаем з всех что можно - все что нельзя books_ex2)
        rooms = Room.objects.exclude(id__in=books_ex2.all().values('room_id')).filter(capacity__gte=capacity)

        return rooms.order_by('price')
    else:
        # эта ветка на тот случай если форма поиска не валидируется браузером ()
        SearchFormData.reset()
        return None

# Проверка бронирования на ошибки (при создании бронирования create_book())
def check_book(booking):
    errors = {}
    # выбираем из Бронирований все, что касаются этого номера (только подтвержденные или в стадии подтверждения)
    room = Booking.objects.filter(room=booking.room.pk, status_conf__in=['1','2'])
    # ищем пересечения по датам
    check = room.all().exclude(Q(checkout__lte=booking.checkin, checkout__lt=booking.checkout) |
                                Q(checkin__gte=booking.checkout, checkin__gt=booking.checkin))
    # если нашлось пересечение, значит запишет ошибку
    if check:
        errors['book'] = True
    # если вместимость номера меньше запрашиваемой, значит запишет ошибку
    if booking.kids + booking.adults > booking.room.capacity:
        errors['capacity'] = True
    if booking.checkin >= booking.checkout:
        errors['date'] = True
    # если бронирование прошло проверку и нет ошибок то False иначе вернет словарь с ошибками
    return False if not errors else errors

def home(request):
    '''
        страница домашняя
    '''
    form = SignForEmailForm()
    if request.method == 'POST' and 'search' in request.POST:
        context = {'room_list': searching_results(request), 'search': True, 'data':SearchFormData}
        return render(request, 'room_list.html', context)
    elif request.method == 'POST' and 'sign_fore_email' in request.POST:
        form = SignForEmailForm(request.POST)
        if form.is_valid():
            form.save()
            send_email_task.delay(form.instance.email)
            return redirect('signup_success')

    # room_list = Room.objects.order_by('price')
    room_list = Room.objects.order_by('category')[::2]
    SearchFormData.reset()
    return render(request, 'room_list.html', {'room_list': room_list, 'main':True, 'form':form})


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
    discount = 1

    if request.method == 'POST' and 'search' in request.POST:
        context = {'room_list': searching_results(request), 'search': True, 'data': SearchFormData}
        return render(request, 'room_list.html', context)

    elif request.method == 'POST' and 'booking' in request.POST:
        form = BookingForm(request.POST)
        if request.user.is_vip:
            discount = (100 - DISCOUNT_COST) / 100
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = Room.objects.get(pk=pk)
            booking.nights = (booking.checkout - booking.checkin).days
            booking.cost = int(booking.nights * booking.room.price * discount)
            errors = check_book(booking)
            if errors == False:
                booking.save()
                send_booking_email_task.delay(booking.id)
                return redirect('success')

        context = {'room_list': room_list, 'search': False, 'form':form, 'errors': errors}
        return render(request, 'booking.html', context)
        # return redirect('fail')

    context = {'room_list': room_list, 'search': True, 'data':SearchFormData}
    return render(request, 'booking.html', context)


def success(request):
    return render(request, 'success.html')

def signup_for_email_success(request):
    return render(request, 'signfor_email_success.html')


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


def booking_expired_tracing():
    # пометили просроченные брони - expire
    try:
        books_ref = Booking.objects.filter(status_conf='2',
                                           deadline_conf__lt=datetime.today().date()).update(status_conf='4')
    except:
        pass
    # законфирмили все брони предыдущие текущей дате (в тестовых целях)
    # books_past = Booking.objects.filter(checkout__lt=datetime.today().date()).update(status_conf='1')


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
            # обновляем БД помечаем все просроченные брони
            # if str(Group.objects.get(user=user.id)) == 'Администратор':
            #     booking_expired_tracing()

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
            user.is_active = False
            user.save()
            user_group = Group.objects.get(name='Гость')
            user.groups.add(user_group)

            # отправляем на email ссылку для активации
            current_site = get_current_site(request)
            subject = 'Активируйте аккаунт ГОСТИШКИ'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_subj_mes_email_task.delay(subject, message, to_email)

            return redirect('confirm_email')
        else:
            return render(request, 'login.html', {'search': False, 'mode':'registr', 'form': form})

    return render(request, 'login.html', {'search': False, 'mode':'registr'})


@login_required
def confirm_email(request):
    '''
        страница-заглушка "подтвердите email для активации аккаунта"
    '''
    return render(request, 'confirm_email.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        mymess = 'Ваш аккаунт активирован!'
        return redirect('profile', user.pk)
    else:
        return redirect('fail')


@login_required
def profile(request, pk):
    '''
        страница "Профиль гостя"
    '''

    form = UploadAvatar()
    if request.method == 'POST' and 'change_avatar' in request.POST:
        form = UploadAvatar(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            print(user)

    user_book = Booking.objects.filter(user=pk).order_by('-checkin')
    actual_book = user_book.filter(checkout__gt=datetime.today().date(), status_conf__in=['1','2'])
    context = {'search': False, 'access': 'success', 'actual':actual_book, 'history':user_book, 'form':form}
    return render(request, 'profile_data.html', context)


@login_required
def cancel_book(request, pk):
    '''
        действие "отмена брони"
    '''

    book = Booking.objects.filter(pk=pk).update(status_conf='3', date_of_cancel=datetime.today().date())

    user = request.user
    return redirect('profile', user.pk)


@login_required
def confirm_book(request, pk):
    '''
        действие "подтверждение брони" ОПЛАТА BRAINTREE
    '''

    book = Booking.objects.filter(pk=pk).update(status_conf='1', date_of_conf=datetime.today().date())

    user = request.user
    return redirect('profile', user.pk)


@login_required
def payment_form(request, user_id, book_id):
    '''
        страница "Форма оплаты"
    '''
    book = Booking.objects.get(pk=book_id)
    # braintere
    if settings.BRAINTREE_PRODUCTION:
        braintree_env = braintree.Environment.Production
    else:
        braintree_env = braintree.Environment.Sandbox
    # Configure Braintree
    braintree.Configuration.configure(
        braintree_env,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC_KEY,
        private_key=settings.BRAINTREE_PRIVATE_KEY,
    )
    try:
        braintree_client_token = braintree.ClientToken.generate({"customer_id": user_id})
    except:
        braintree_client_token = braintree.ClientToken.generate({})

    context = {'braintree_client_token': braintree_client_token, 'book':book, 'user_id':user_id}
    return render(request, 'payment_form.html', context)


@login_required
def payment(request, user_id, book_id):
    '''
        действие  ОПЛАТА BRAINTREE
    '''
    book = Booking.objects.get(pk=book_id)
    user = CustomUser.objects.get(pk=user_id)
    nonce_from_the_client = request.POST['paymentMethodNonce']
    customer_kwargs = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }
    customer_create = braintree.Customer.create(customer_kwargs)
    customer_id = customer_create.customer.id
    result = braintree.Transaction.sale({
        "amount": book.cost,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })
    if result.is_successful:
        print(result)
        return redirect('payment_success')
    else: return redirect('fail')

def payment_success(request):
    return render(request, 'payment_success.html')