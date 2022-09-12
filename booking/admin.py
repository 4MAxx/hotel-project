from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

from booking.models import Category, Room, Booking, CustomUser, SignedForEmail


@admin.register(Booking)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'room',
                    'user',
                    'checkin',
                    'checkout',
                    'adults',
                    'kids',
                    'status_conf',
                    'date_of_book',
                    'deadline_conf',
                    'date_of_conf']
    fieldsets = (
        ('Основная информация', {'fields': ('id', 'date_of_book', 'room', 'user', 'cost',)}),
        ('Статус бронирования', {'fields': ('status_conf', 'deadline_conf',
                                            )}),
        ('Дата оплаты / отмены', {'fields': ('date_of_conf', 'date_of_cancel',
                                    )}),
        ('Параметры бронирования', {'fields': ('checkin',
                                               'checkout',
                                               'nights',
                                               'adults',
                                               'kids',
                                               'special',
                                                )}),
        ('Фактические даты заезда / выезда', {'fields': ('date_of_arrive', 'date_of_depart',
                                             )}),

    )
    readonly_fields = ('id',
                       'room',
                       'user',
                       'checkin',
                       'checkout',
                       'nights',
                       'cost',
                       'status_conf',
                       'deadline_conf',
                       'date_of_conf',
                       'date_of_book',
                       'date_of_cancel')
    ordering = ('checkin',)


admin.site.register(Category)


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
        ('Персональная информация', {'fields': ('last_name', 'first_name', 'phone', 'gender',
                                                'img', 'adress', 'doc1', 'doc2', 'doc3',
                                                )})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'groups')}
         ),
    )
    readonly_fields = ('is_active','groups','password')
    search_fields = ('email',)
    ordering = ('email',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()
        if not is_superuser:
            disabled_fields |= {
                'is_staff',
                'email',
                'is_superuser',
                'groups',
                'user_permissions',
                'password',
            }
        # Prevent non-superusers from editing their own permissions
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form


@admin.register(SignedForEmail)
class SignedForEmailAdmin(admin.ModelAdmin):
    list_display = ['email',
                    'date_of_sign',
                    'date_last_send',
                    ]

    readonly_fields = ('email', 'date_of_sign','date_last_send',)