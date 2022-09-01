import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
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
    capacity = models.IntegerField(default=0, verbose_name = 'Вместииость')
    beds = models.IntegerField(default=0, verbose_name = 'Кроватей')
    checkin = models.DateField(auto_now_add=False, null=True, blank=True, verbose_name = 'Заселение')
    checkout = models.DateField(auto_now_add=False, null=True, blank=True, verbose_name = 'Убытие')
    status = models.BooleanField(default=True, verbose_name = 'Свободен/Занят')
    img = models.ImageField(upload_to='booking/img/room', blank=True, null=True, verbose_name = 'Фото')
    slide1 = models.ImageField(upload_to='booking/img/room-slide', blank=True, null=True, verbose_name = 'Слайд 1')
    slide2 = models.ImageField(upload_to='booking/img/room-slide', blank=True, null=True, verbose_name = 'Слайд 2')
    slide3 = models.ImageField(upload_to='booking/img/room-slide', blank=True, null=True, verbose_name = 'Слайд 3')

    def __str__(self):
        return f'{str(self.number)} - {self.category}'

class Booking(models.Model):
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['checkin', 'status_conf']

    STATUSES = [('2', 'wait'),
                ('1', 'confirm'),
                ('3', 'cancel'),
                ('4', 'expire'),
                ('5', 'success')]
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False, verbose_name = 'Гость')
    special = models.CharField(max_length=1000, blank=True, null=True, verbose_name = 'Особые пожелания')
    date_of_book = models.DateField(auto_now_add=True, null=False, blank=False, verbose_name = 'Дата бронирования')
    room = models.ForeignKey(Room, on_delete=models.PROTECT, null=False, blank=False, verbose_name = 'Номер')
    checkin = models.DateField(auto_now_add=False, null=False, blank=False, verbose_name = 'Заселение')
    checkout = models.DateField(auto_now_add=False, null=False, blank=False, verbose_name = 'Убытие')
    status_conf = models.CharField(max_length=1, choices=STATUSES, default='1', verbose_name = 'Статус брони')
    deadline_conf = models.DateField(blank=True, null=True, verbose_name = 'Срок оплаты')
    date_of_conf = models.DateField(blank=True, null=True, verbose_name = 'Дата оплаты')

    def __str__(self):
        return f'№: {self.room} - Статус: {self.get_status_conf_display()}'

    def save(self, *args, **kwargs):
        if self.deadline_conf is None:
            self.deadline_conf = datetime.datetime.now().date() + datetime.timedelta(days=1)
        super(Booking, self).save(*args, **kwargs)