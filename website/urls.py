from django.contrib import admin
from django.urls import path
from app_allen import views as app_allen_views

urlpatterns = [
    path('', app_allen_views.index),
    path('index', app_allen_views.index),
    path('task', app_allen_views.task),
    path('test', app_allen_views.test),
    path('tanji_customer_export', app_allen_views.tanji_customer_export),
    path('tanji_receive', app_allen_views.tanji_receive),
]
