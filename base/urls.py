from django.urls import path
from . import views

urlpatterns=[
    path('register/',views.registerPage ,name='register'),
    path('login/',views.loginPage ,name='login'),
    path('logout/',views.logoutPage ,name='logout'),
    path('',views.home ,name='home'),
    path('room/<str:pk>/',views.room , name='room'),
    path('room-form/',views.createRoom ,name='room-form'),
    path('update/<str:pk>/', views.updateForm ,name='update'),
    path('delete/<str:pk>/', views.deleteRoom ,name='delete'),
    path('deleteMmessage/<str:pk>/', views.deleteMessage ,name='deleteMessage'),
    path('profile/<str:pk>/',views.userProfile , name='profile'),
    path('update-user/',views.updateUser , name='update-user'),
    path('topics/',views.topicPage , name='topics'),
    path('activity/',views.activityPage , name='activity'),
    
]