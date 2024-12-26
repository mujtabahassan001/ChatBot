from django.urls import path

from . import views


urlpatterns = [
    path('chat/<str:room_name>/', views.chat, name='chat'),
    path('enter-room/', views.enter_room, name='enter_room'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
]