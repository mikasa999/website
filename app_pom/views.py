from django.shortcuts import render, HttpResponse
from django.forms import ModelForm
from app_pom import models

class PomModelForm(ModelForm):
    class Meta:
        model = models.run_settings
        fields = ['pom_create_date', 'pom_scan_platform', 'pom_scan_page_num']

def pom_index(request):
    """首页"""
    return render(request, 'pom_index.html')

def pom_task(request):
    """任务页面，同时可以接受post传值"""

    return render(request, 'pom_task.html')

def pom_test(request):
    """测试modelForm组件，测试完可以删除"""
    form = PomModelForm()
    return render(request, 'pom_test.html', {"form": form})
