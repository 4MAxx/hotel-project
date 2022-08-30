from django.contrib import admin

# Register your models here.
from booking.models import Category, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'category', 'status', 'checkin', 'checkout', 'price', 'capacity', 'beds', 'text']

admin.site.register(Category)