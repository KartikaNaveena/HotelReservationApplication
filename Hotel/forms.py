from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django import forms

class RegisterForm(UserCreationForm):
    
    email = forms.EmailField(required=True,
                             widget=forms.TextInput)
    class Meta:
     model=User
     fields=('username','email','password1','password2')
class BookingForm(forms.Form):
    room_type = forms.ModelChoiceField(queryset=RoomType.objects.all())
    check_in = forms.DateField()
    check_out = forms.DateField()

