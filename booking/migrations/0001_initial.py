# Generated by Django 4.1 on 2022-08-28 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0, unique=True)),
                ('text', models.TextField(max_length=500)),
                ('price', models.IntegerField(default=0)),
                ('size', models.IntegerField(default=0)),
                ('capacity', models.IntegerField(default=0)),
                ('beds', models.IntegerField(default=0)),
                ('checkin', models.DateTimeField()),
                ('checkout', models.DateTimeField()),
                ('status', models.BooleanField(default=False)),
                ('img', models.ImageField(blank=True, null=True, upload_to='blog/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='booking.category')),
            ],
        ),
    ]