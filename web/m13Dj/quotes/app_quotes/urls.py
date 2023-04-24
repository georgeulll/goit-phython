from django.contrib import admin
from django.urls import path

from . import views

app_name = 'app_quotes'

urlpatterns = [
    path('', views.main, name='root'),
    path('upload_quotes/', views.upload_quotes, name='upload_quotes'),
    path('quotes/', views.quotes, name='quotes'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_tags/', views.add_tags, name='add_tags'),
    path('author/<int:id>/', views.author_detail, name='author_detail')
]