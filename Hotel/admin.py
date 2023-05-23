from django.contrib import admin
from .models import Hotels,Rooms,Booking,RoomType
# Register your models here.
admin.site.register(Hotels)
admin.site.register(Rooms)
admin.site.register(Booking)
admin.site.register(RoomType)
