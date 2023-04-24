from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signupuser, name='signup'),
    path('signin/', views.loginuser, name='signin'),
    path('logout/', views.logoutuser, name='logout'),
]