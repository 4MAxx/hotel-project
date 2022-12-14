# Generated by Django 4.1 on 2022-09-03 16:20

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_vip', models.BooleanField(default=False, verbose_name='VIP')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='??????????????')),
                ('gender', models.CharField(choices=[('??', '??????????????'), ('??', '??????????????')], default='', max_length=1, verbose_name='??????')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': '?????????????????? ??????????????',
                'verbose_name_plural': '?????????????????? ??????????????',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0, unique=True, verbose_name='??????????')),
                ('text', models.TextField(max_length=500, verbose_name='???????????????? ????????????')),
                ('price', models.IntegerField(default=0, verbose_name='????????')),
                ('size', models.IntegerField(default=0, verbose_name='??????????????')),
                ('capacity', models.IntegerField(default=0, verbose_name='??????????????????????')),
                ('beds', models.IntegerField(default=0, verbose_name='????????????????')),
                ('checkin', models.DateField(blank=True, null=True, verbose_name='??????????????????')),
                ('checkout', models.DateField(blank=True, null=True, verbose_name='????????????')),
                ('status', models.BooleanField(default=True, verbose_name='????????????????/??????????')),
                ('img', models.ImageField(blank=True, null=True, upload_to='booking/img/room', verbose_name='????????')),
                ('slide1', models.ImageField(blank=True, null=True, upload_to='booking/img/room-slide', verbose_name='?????????? 1')),
                ('slide2', models.ImageField(blank=True, null=True, upload_to='booking/img/room-slide', verbose_name='?????????? 2')),
                ('slide3', models.ImageField(blank=True, null=True, upload_to='booking/img/room-slide', verbose_name='?????????? 3')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='booking.category', verbose_name='??????????????????')),
            ],
            options={
                'verbose_name': '??????????',
                'verbose_name_plural': '????????????',
                'ordering': ['category'],
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('special', models.CharField(blank=True, max_length=1000, null=True, verbose_name='???????????? ??????????????????')),
                ('date_of_book', models.DateField(auto_now_add=True, verbose_name='???????? ????????????????????????')),
                ('checkin', models.DateField(verbose_name='??????????????????')),
                ('checkout', models.DateField(verbose_name='????????????')),
                ('status_conf', models.CharField(choices=[('2', 'wait'), ('1', 'confirm'), ('3', 'cancel'), ('4', 'expire'), ('5', 'success')], default='1', max_length=1, verbose_name='???????????? ??????????')),
                ('deadline_conf', models.DateField(blank=True, null=True, verbose_name='???????? ????????????')),
                ('date_of_conf', models.DateField(blank=True, null=True, verbose_name='???????? ????????????')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='booking.room', verbose_name='??????????')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='??????????')),
            ],
            options={
                'verbose_name': '????????????????????????',
                'verbose_name_plural': '????????????????????????',
                'ordering': ['checkin', 'status_conf'],
            },
        ),
    ]
