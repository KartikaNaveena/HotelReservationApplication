# Generated by Django 4.1.4 on 2023-05-05 12:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Hotel', '0005_alter_rooms_room_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('booking_id', models.CharField(default='null', max_length=100)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='booking',
            name='room',
        ),
        migrations.DeleteModel(
            name='RoomType',
        ),
        migrations.RemoveField(
            model_name='rooms',
            name='hotel_connected',
        ),
        migrations.AddField(
            model_name='rooms',
            name='hotel',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='Hotel.hotels'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rooms',
            name='room_type',
            field=models.CharField(choices=[('1', 'premium'), ('2', 'deluxe'), ('3', 'basic')], max_length=50),
        ),
        migrations.DeleteModel(
            name='Booking',
        ),
        migrations.AddField(
            model_name='reservation',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hotel.rooms'),
        ),
    ]
