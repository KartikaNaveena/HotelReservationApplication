from . import views
from django.urls import path

urlpatterns = [
        path("", views.HotelList.as_view(), name="home"),
     path('staff/', views.staff_panel, name='staffpanel'),
    path('staff/', views.staff_panel, name='panel'),
    path('user/signup', views.user_sign_up,name="usersignup"),
    path('user/login', views.user_log_page,name="userloginpage"),
    path('staff/login', views.staff_log_page,name="staffloginpage"),
    path('staff/signup', views.staff_sign_up,name="staffsignup"),
    path('logout/', views.logoutuser,name="logout"),
     path('dashboard/', views.reservations,name="reservations"),
      path("search/", views.SearchResultsView.as_view(), name="search_results"),
    path('<int:hotel_id>/<int:room_id>/delete-room/', views.delete_room, name='delete_room'),
     path("hotel/<int:hotel_id>",views.hotel_detail,name="hotel_detail"),
    path("book/room/<int:hotel_id>",views.book_room,name="book_room"),
      path('<int:hotel_id>/<int:room_id>/edit-room/', views.edit_room, name='edit_room'),
     path('hotel-list/', views.hotel_list, name='hotel_list_for_staff'),
     path('delete_hotel/<int:hotel_id>/', views.delete_hotel, name='delete_hotel'),
      path('hotel-detail_staff/<int:hotel_id>/', views.hotel_detail_staff, name='hotel_detail_staff'),
      path('hotel-detail-staff/<int:hotel_id>/add-room/', views.add_room, name='add_room'),
]