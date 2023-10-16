from django.contrib import admin
from django.urls import path
from app_tanji import views as tanji_views
from app_pom import views as pom_views
from app_fenci import views as fenci_views

urlpatterns = [
    # 首页
    path('', fenci_views.fenci_index),
    # 舆情处理
    path('pom/index', pom_views.pom_index),
    path('pom/task', pom_views.pom_task),
    path('pom/test', pom_views.pom_test),
    # 探迹
    path('tanji/index', tanji_views.tanji_index),
    path('tanji/receive', tanji_views.tanji_receive),
    #分词
    path('fenci/index', fenci_views.fenci_index),
    path('fenci/zcg', fenci_views.fenci_zcg),
    path('fenci/qxc', fenci_views.fenci_qxc),
    path('fenci/fywc', fenci_views.fenci_fywc),
    path('fenci/ywc', fenci_views.fenci_ywc),
    path('fenci/fc', fenci_views.fenci_fc),
]
