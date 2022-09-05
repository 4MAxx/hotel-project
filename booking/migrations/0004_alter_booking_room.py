# Generated by Django 4.1 on 2022-09-05 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_booking_adults_booking_kids_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rooms', to='booking.room', verbose_name='Номер'),
        ),
    ]
