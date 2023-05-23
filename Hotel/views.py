from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,redirect,get_object_or_404
from Hotel.forms import *
from .models import *
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import messages
from django.views import generic
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.


class HotelList(generic.ListView):
    model = Hotels
    context_object_name = 'hotel_list' 
    queryset =Hotels.objects.all()
    template_name = 'index.html'



class SearchResultsView(generic.ListView):
    model = Hotels
    template_name = "search_results.html"

    def get_queryset(self): 
        query = self.request.GET.get("q")
        object_list = Hotels.objects.filter(
            Q(location__icontains=query) | Q(name__icontains=query)
        )
        return object_list

def user_sign_up(request):
    if request.method =="POST":
        user_name = request.POST['username']
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.warning(request,"Password didn't matched")
            return redirect('userloginpage')
        
        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request,"Username Already Available")
                return redirect('home')
        except:
            pass
            

        new_user = User.objects.create_user(username=user_name,password=password1)
        new_user.is_superuser=False
        new_user.is_staff=False
        new_user.save()
        messages.success(request,"Registration Successfull")
        return redirect("userloginpage")
    else:
        form=RegisterForm()
    return render(request,'register.html',{'form':form})

def staff_sign_up(request):
    if request.method =="POST":
        user_name = request.POST['username']
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.success(request,"Password didn't Matched")
            return redirect('staffloginpage')
        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request,"Username Already Exist")
                return redirect("staffloginpage")
        except:
            pass
        
        new_user = User.objects.create_user(username=user_name,password=password1)
        new_user.is_superuser=False
        new_user.is_staff=True
        new_user.save()
        messages.success(request," Staff Registration Successfull")
        return redirect("staffloginpage")
    else:
        form=RegisterForm()
    return render(request,'register.html',{'form':form})

def user_log_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        try:
            if user.is_staff:
                
                messages.error(request,"Incorrect username or Password")
                return redirect('staffloginpage')
        except:
            pass
        
        if user is not None:
            login(request,user)
            messages.success(request,"successful logged in")
            print("Login successfull")
            return redirect('home')
        else:
            messages.warning(request,"Incorrect username or password")
            return redirect('userloginpage')

    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"form":form})

def logoutuser(request):
    if request.method =='GET':
        logout(request)
        messages.success(request,"Logged out successfully")
        print("Logged out successfully")
        return redirect('home')
    else:
        print("logout unsuccessfull")
        return redirect('userloginpage')

def staff_log_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        
        if user.is_staff:
            login(request,user)
            return redirect('hotel_list_for_staff')
        
        else:
            messages.success(request,"Incorrect username or password")
            return redirect('staffloginpage')
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"form":form})

def staff_panel(request):
    return render(request,'panel.html')


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotels, id=hotel_id)
    return render(request, 'hotel_detail.html', {'hotel': hotel})

def book_room(request, hotel_id):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            hotel = get_object_or_404(Hotels, id=hotel_id)
            room_type = form.cleaned_data['room_type']
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            
            # Find an available room of the selected type at the selected hotel
            booked_rooms = Booking.objects.filter(
                room__hotel=hotel,
                room__room_type=room_type,
                check_out__gt=check_in,
                check_in__lt=check_out,
            ).values_list('room__number', flat=True)
            
            available_rooms = Rooms.objects.filter(
                hotel=hotel,
                room_type=room_type,
            ).exclude(number__in=booked_rooms)
            
            if available_rooms.exists():
                room = available_rooms.first()
                price = room.price * (check_out - check_in).days
                
                # Create the booking
                booking = Booking.objects.create(
                    room=room,
                    guest=request.user,
                    check_in=check_in,
                    check_out=check_out,
                    price=price,
                )
                
                return render(request, 'booking_confirmation.html', {'booking': booking})
            else:
                return render(request, 'no_rooms_available.html')
    else:
        form = BookingForm()
        
    return render(request, 'bookroom.html', {'form': form})
@login_required
def reservations(request):
    bookings = Booking.objects.filter(guest=request.user)
    return render(request, 'reservations.html', {'bookings': bookings})

def hotel_list(request):
    hotels = Hotels.objects.all()
    context = {'hotels': hotels}
    return render(request, 'hotel_list.html', context)

def hotel_detail_staff(request, hotel_id):
    hotel = get_object_or_404(Hotels, id=hotel_id)
    rooms = Rooms.objects.filter(hotel=hotel)
    bookings = Booking.objects.filter(room__in=rooms)
    context = {
        'hotel': hotel,
        'rooms': rooms,
        'bookings': bookings,
    }
    return render(request, 'hotel_detail_staff.html', context)

def delete_room(request, hotel_id, room_id):
    hotel = get_object_or_404(Hotels, id=hotel_id)
    room = get_object_or_404(Rooms, id=room_id, hotel=hotel)
    room.delete()
    return redirect('hotel_detail_staff', hotel_id=hotel_id)

def edit_room(request, hotel_id, room_id):
    hotel = get_object_or_404(Hotels, id=hotel_id)
    room = get_object_or_404(Rooms, id=room_id, hotel=hotel)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('hotel_detail_staff', hotel_id=hotel_id)
    else:
        form = RoomForm(instance=room)
    context = {
        'hotel': hotel,
        'room': room,
        'form': form,
    }
    return render(request, 'edit_room.html', context)
def add_room(request, hotel_id):
    hotel = get_object_or_404(Hotels, id=hotel_id)
    if request.method == 'POST':
        form = RoomaddForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            return redirect('hotel_detail_staff', hotel_id=hotel_id)
    else:
        form = RoomaddForm()
    context = {
        'hotel': hotel,
        'form': form,
    }
    return render(request, 'add_room.html', context)

def delete_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotels, id=hotel_id)
    hotel.delete()
    return redirect('hotel_list_for_staff')
            
