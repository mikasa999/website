from django.contrib import admin
from django.urls import path
from app_tanji import views as tanji_views
from app_pom import views as pom_views
from app_fenci import views as fenci_views

urlpatterns = [
    # 首页
    path('', fenci_views.fenci_index),
    path('index', fenci_views.fenci_index),
    # 舆情处理
    path('pom', pom_views.pom_index),
    path('pom/task', pom_views.pom_task),
    path('pom/test', pom_views.pom_test),
    # 探迹
    path('tanji', tanji_views.tanji_index),
    path('tanji/receive', tanji_views.tanji_receive),
    #分词
    path('fenci', fenci_views.fenci_index),
]
