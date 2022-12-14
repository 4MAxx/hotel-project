import datetime

from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import Group, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

# Create your models here.
from booking.managers import CustomUserManager
from django.shortcuts import redirect


class Category(models.Model):
    class Meta:
        verbose_name = 'Категории номеров'
        verbose_name_plural = 'Категории номеров'

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'
        ordering = ['category']

    number = models.IntegerField(default=0, unique=True, verbose_name = 'Номер')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name = 'Категория')
    text = models.TextField(max_length=500, verbose_name = 'Описание номера')
    price = models.IntegerField(default=0, verbose_name = 'Цена')
    size = models.IntegerField(default=0, verbose_name = 'Площадь')
    capacity = models.IntegerField(default=0, verbose_name = 'Вместимость')
    beds = models.IntegerField(default=0, verbose_name = 'Кроватей')
    checkin = models.DateField(auto_now_add=False, null=True, blank=True, verbose_name = 'Заселение')
    checkout = models.DateField(auto_now_add=False, null=True, blank=True, verbose_name = 'Убытие')
    status = models.BooleanField(default=True, verbose_name = 'Свободен/Занят')
    img = models.ImageField(upload_to='booking/img/room', blank=True, null=True, verbose_name = 'Фото')
    slide1 = models.ImageField(upload_to='booking/img/room-slide', blank=True, null=True, verbose_name = 'Слайд 1')
    slide2 = models.ImageField(upload_to='booking/img/room-slide', blank=True, null=True, verbose_name = 'Слайд 2')
    slide3 = models.ImageField(upload_to='booking/img/room-slide', blank=True, null=True, verbose_name = 'Слайд 3')

    def __str__(self):
        return f'{self.category} ={str(self.number)}='


class Booking(models.Model):
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['checkin', 'status_conf']

    STATUSES = [('1', 'confirm'),
                ('2', 'wait'),
                ('3', 'cancel'),
                ('4', 'expire'),
                ('5', 'success')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False,
                             verbose_name = 'Гость')
    special = models.CharField(max_length=1000, blank=True, null=True, verbose_name = 'Особые пожелания')
    date_of_book = models.DateField(auto_now_add=True, null=False, blank=False, verbose_name = 'Дата бронирования')
    room = models.ForeignKey(Room, on_delete=models.PROTECT, null=False, blank=False, verbose_name = 'Номер', related_name='rooms')
    checkin = models.DateField(auto_now_add=False, null=False, blank=False, verbose_name = 'Заселение')
    checkout = models.DateField(auto_now_add=False, null=False, blank=False, verbose_name = 'Убытие')
    adults = models.IntegerField(default=1, verbose_name = 'Взрослых')
    kids = models.IntegerField(default=0, verbose_name='Детей')
    status_conf = models.CharField(max_length=1, choices=STATUSES, default='2', verbose_name = 'Статус брони')
    deadline_conf = models.DateField(blank=True, null=True, verbose_name = 'Срок оплаты')
    date_of_conf = models.DateField(blank=True, null=True, verbose_name = 'Дата оплаты')
    date_of_cancel = models.DateField(blank=True, null=True, verbose_name='Дата отмены')
    nights = models.IntegerField(default=1, verbose_name='Ночей')
    cost = models.IntegerField(default=0, verbose_name='Общая стоимость')
    date_of_arrive = models.DateField(blank=True, null=True, verbose_name='Дата заезда')
    date_of_depart = models.DateField(blank=True, null=True, verbose_name='Дата выезда')

    def __str__(self):
        return f'№: {self.id} | {self.room} | Статус: {self.get_status_conf_display()}'

    def check_dates(self):
        '''
            вызывает исключение если пересекаются даты бронирования (например, из админки)
        '''
        room = Booking.objects.filter(room=self.room.pk, status_conf__in=['1','2'])
        check = room.all().exclude(Q(checkout__lte=self.checkin, checkout__lt=self.checkout) |
                                            Q(checkin__gte=self.checkout, checkin__gt=self.checkin))
        # если нашлось пересечение, вернет False
        if check: return False

        return True

    def save(self, *args, **kwargs):
        if self.deadline_conf is None:
            self.deadline_conf = datetime.datetime.now().date() + datetime.timedelta(days=1)
        if self.check_dates() == False:
            raise ValueError('Допущено пересечение дат по бронированию, выберите другой промежуток дат')
        super(Booking, self).save(*args, **kwargs)


class CustomUser(AbstractUser):
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    GENDERS = (('м', 'мужской'),
                ('ж', 'женский'),)
    email = models.EmailField(_('email address'), unique=True)
    email_confirmed = models.BooleanField(default=False)
    is_vip = models.BooleanField(default=False, verbose_name = 'VIP')
    phone = models.CharField(max_length=20,blank=True, null=True, verbose_name = 'Телефон')
    gender = models.CharField(max_length=1, choices=GENDERS, default='', verbose_name = 'Пол')
    img = models.ImageField(upload_to='booking/img/avatar', blank=True, null=True, verbose_name='Аватарка')
    adress = models.CharField(max_length=200, blank=True, null=True, verbose_name = 'Адрес проживания')
    doc1 = models.ImageField(upload_to='booking/img/docs', blank=True, null=True, verbose_name='Фото документа 1')
    doc2 = models.ImageField(upload_to='booking/img/docs', blank=True, null=True, verbose_name='Фото документа 2')
    doc3 = models.ImageField(upload_to='booking/img/docs', blank=True, null=True, verbose_name='Фото документа 3')

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.last_name} {self.first_name[0]}. - {self.email}'
        else: return self.email

class SignedForEmail(models.Model):

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'

    email = models.EmailField(_('email address'), unique=True)
    date_of_sign = models.DateField(auto_now_add=True, verbose_name='Дата подписки')
    date_last_send = models.DateField(blank=True, null=True, verbose_name='Дата последней рассылки')

    def __str__(self):
        return self.email