from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, include
from api import views
urlpatterns = [
    path('cms/', views.CMS),
    path('cms_confirm/',views.CMS_confirm),
    # path('fr/',views.FR),
]

