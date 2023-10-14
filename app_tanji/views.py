from django.shortcuts import render, HttpResponse
from django.forms import ModelForm
from app_tanji import models

def tanji_index(request):
    """导出探迹客户的操作页面"""
    return render(request, 'tanji_index.html')

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

        # def run():
        #     from tanji.tanji_customer_export import tanji_customer_export
        #     customer = tanji_customer_export()
        #     customer.run()

        return render(request, 'tanji_receive.html')


