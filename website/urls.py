from django.contrib import admin
from django.urls import path
from app_tanji import views as tanji_views
from app_pom import views as pom_views

urlpatterns = [
    # 首页
    path('', pom_views.index),
    # path('index', pom_views.index),
    # 舆情处理
    path('pom', pom_views.index),
    path('pom/task', pom_views.task),
    path('pom/test', pom_views.test),
    # 探迹
    path('tanji', tanji_views.tanji_customer_export),
    path('tanji/receive', tanji_views.tanji_receive)
]
