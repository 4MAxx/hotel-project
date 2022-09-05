from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

from booking.models import Category, Room, Booking, CustomUser


@admin.register(Booking)
class BookAdmin(admin.ModelAdmin):
    list_display = ['room',
                    'user',
                    'checkin',
                    'checkout',
                    'adults',
                    'kids',
                    'status_conf',
                    'date_of_book',
                    'deadline_conf',
                    'date_of_conf']
    readonly_fields = ('deadline_conf', 'status_conf', 'date_of_conf')
    ordering = ('checkin',)

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
                    'size',
                    'text']
    readonly_fields = ('checkin', 'checkout',)

admin.site.register(Category)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email',
                    'is_vip',
                    'last_name',
                    'first_name',
                    'phone',
                    'is_staff',
                    ]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Права', {'fields': ('is_staff', 'is_active', 'groups')}),
        ('Персональная информация', {'fields': ('last_name', 'first_name', 'phone', 'gender')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'groups')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)