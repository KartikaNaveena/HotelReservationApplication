from . import views
from django.urls import path

urlpatterns = [
  
     path('staff/', views.staff_panel, name='staffpanel'),
    path('staff/', views.staff_panel, name='panel'),
    path('user/signup', views.user_sign_up,name="usersignup"),
    path('user/login', views.user_log_page,name="userloginpage"),
    path('staff/login', views.staff_log_page,name="staffloginpage"),
    path('staff/signup', views.staff_sign_up,name="staffsignup"),
    path('logout/', views.logoutuser,name="logout"),
      path("search/", views.SearchResultsView.as_view(), name="search_results"),
    path("", views.HotelList.as_view(), name="home"),
     path("hotel/<slug:slug>",views.HotelDetail.as_view(),name="hotel_detail"),
       path("hotel/book/<slug:slug>", views.book_room_page,name="bookroompage"),
]