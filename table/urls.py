from django.urls import path

from table import views

urlpatterns =[
    path('',views.upload_excel),
    path("datatest/<img>",views.data_test,name="test")


]