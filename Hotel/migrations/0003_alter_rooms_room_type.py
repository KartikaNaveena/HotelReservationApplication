# Generated by Django 4.1.4 on 2023-05-05 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel', '0002_remove_rooms_hotel_rooms_hotel_connected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rooms',
            name='room_type',
            field=models.CharField(choices=[('premium', 'premium'), ('deluxe', 'deluxe'), ('basic', 'basic')], max_length=50),
        ),
    ]