from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    number = models.IntegerField(default=0, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    text = models.TextField(max_length=500)
    price = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    beds = models.IntegerField(default=0)
    checkin = models.DateField(auto_now_add=False, null=True, blank=True)
    checkout = models.DateField(auto_now_add=False, null=True, blank=True)
    status = models.BooleanField(default=True)
    img = models.ImageField(upload_to='booking/img/room', blank=True, null=True)
    slide1 = models.ImageField(upload_to='booking/img/room-slide', blank=True, null=True)
    slide2 = models.ImageField(upload_to='booking/img/room-slide', blank=True, null=True)
    slide3 = models.ImageField(upload_to='booking/img/room-slide', blank=True, null=True)
