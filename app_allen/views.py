from django.shortcuts import render, HttpResponse
from django.forms import ModelForm
from app_allen import models

class PomModelForm(ModelForm):
    class Meta:
        model = models.pom_run_config
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

def tanji_customer_export(request):
    """导出探迹客户的操作页面"""
    return render(request, 'tanji_customer_export.html')

def tanji_receive(request):
    """探迹任务接收处理"""
    if request.method == 'GET':
        return render(request, 'tanji_receive.html')
    if request.method == 'POST':
        tanji_huashu = request.POST.get('tanji_huashu')
        tanji_huashu_banben = request.POST.get('tanji_huashu_banben')
        tanji_duandian = '开启' if request.POST.get('tanji_duandian') == 'on' else '关闭'
        tanji_denglu = '开启' if request.POST.get('tanji_denglu') == 'on' else '关闭'
        tanji_username = request.POST.get('tanji_username')
        tanji_password = request.POST.get('tanji_password')

        data = {
            'tanji_huashu': tanji_huashu,
            'tanji_huashu_banben': tanji_huashu_banben,
            'tanji_duandian': tanji_duandian,
            'tanji_denglu': tanji_denglu,
            'tanji_username': tanji_username,
            'tanji_password': tanji_password,
        }

        def run():
            from app_allen.utils.tanji_customer_export import tanji_customer_export
            customer = tanji_customer_export()
            customer.run()

        return render(request, 'tanji_receive.html', data, run())


