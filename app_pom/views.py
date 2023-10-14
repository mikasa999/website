from django.shortcuts import render, HttpResponse
from django.forms import ModelForm
from app_pom import models

class PomModelForm(ModelForm):
    class Meta:
        model = models.run_settings
        fields = ['pom_create_date', 'pom_scan_platform', 'pom_scan_page_num']

def index(request):
    """首页"""
    return render(request, 'index.html')

def task(request):
    """任务页面，同时可以接受post传值"""

    return render(request, 'task.html')

def test(request):
    """测试modelForm组件，测试完可以删除"""
    form = PomModelForm()
    return render(request, 'test.html', {"form": form})
