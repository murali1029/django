from django.contrib import admin
from django.urls import path
from .views import ToDoList
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('', ToDoList.as_view(), name= 'home'),
]