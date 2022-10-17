from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, include
from account import views
urlpatterns = [
    path('login/', views.login),
    path('display/', views.display),
    path('add/', views.add),
    path('delete/', views.delete),
    path('edit/', views.edit),
    path('query/', views.query),
]

