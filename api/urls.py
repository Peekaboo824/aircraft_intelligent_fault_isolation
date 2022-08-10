from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, include
from api import views
urlpatterns = [
    path('cas/', views.CAS),
    path('cas_confirm/',views.CAS_confirm),
    path('cms/', views.CMS),
    path('cms_confirm/',views.CMS_confirm),
    path('fr/',views.FR),
    path('fr_confirm/',views.FR_confirm),
]

