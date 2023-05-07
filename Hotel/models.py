
from django.db import models

from django.contrib.auth.models import User
# Create your models here.

 


class Hotels(models.Model):
    
    name = models.CharField(max_length=30,unique=True)
    owner = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    state = models.CharField(max_length=50,default="maharashtra")
    country = models.CharField(max_length=50,default="india")
    description=models.CharField(max_length=200)
    slug=models.SlugField(max_length=100,unique=True)
    def __str__(self):
        return self.name

class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name
class Rooms(models.Model):
    ROOM_STATUS = ( 
    ("1", "available"), 
    ("2", "not available"),    
    ) 
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    capacity = models.IntegerField()
    price = models.IntegerField()
    size = models.IntegerField()
    hotel = models.ForeignKey(Hotels, on_delete = models.CASCADE)
    status = models.CharField(choices =ROOM_STATUS,max_length = 15)
    number = models.IntegerField()
    def __str__(self):
        return self.hotel.name

class Booking(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, related_name='bookings')
    guest = models.CharField(max_length=100)
    check_in = models.DateField()
    check_out = models.DateField()
    price = models.IntegerField(null=True)
    def __str__(self):
        return f'{self.guest_name} - {self.room}'