from django.contrib import admin

# Register your models here.
from booking.models import Category, Room, Booking


@admin.register(Booking)
class BookAdmin(admin.ModelAdmin):
    list_display = ['room',
                    'user',
                    'date_of_book',
                    'checkin',
                    'checkout',
                    'status_conf',
                    'deadline_conf',
                    'date_of_conf']
    readonly_fields = ('deadline_conf', 'status_conf', 'date_of_conf')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['number',
                    'category',
                    'status',
                    'checkin',
                    'checkout',
                    'price',
                    'capacity',
                    'beds',
                    'text']

admin.site.register(Category)
