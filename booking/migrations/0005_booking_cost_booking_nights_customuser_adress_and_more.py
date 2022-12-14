# Generated by Django 4.1 on 2022-09-09 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_alter_booking_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='cost',
            field=models.IntegerField(default=0, verbose_name='Общая стоимость'),
        ),
        migrations.AddField(
            model_name='booking',
            name='nights',
            field=models.IntegerField(default=1, verbose_name='Ночей'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='adress',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Адрес проживания'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='doc1',
            field=models.ImageField(blank=True, null=True, upload_to='booking/img/docs', verbose_name='Фото документа 1'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='doc2',
            field=models.ImageField(blank=True, null=True, upload_to='booking/img/docs', verbose_name='Фото документа 2'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='doc3',
            field=models.ImageField(blank=True, null=True, upload_to='booking/img/docs', verbose_name='Фото документа 3'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='booking/img/avatar', verbose_name='Аватарка'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status_conf',
            field=models.CharField(choices=[('1', 'confirm'), ('2', 'wait'), ('3', 'cancel'), ('4', 'expire'), ('5', 'success')], default='2', max_length=1, verbose_name='Статус брони'),
        ),
    ]
