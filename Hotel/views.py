from django.http import HttpResponse 
from django.shortcuts import render,redirect
from Hotel.forms import *
from .models import *
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import messages
from django.views import generic
from django.db.models import Q

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
            return redirect('staffpanel')
        
        else:
            messages.success(request,"Incorrect username or password")
            return redirect('staffloginpage')
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"form":form})

def staff_panel(request):
    return render(request,'panel.html')

class HotelDetail(generic.DetailView):
    model=Hotels
    template_name='hotel_detail.html'


def book_room_page(request):
    model=Hotels
    template_name ='bookroom.html'
