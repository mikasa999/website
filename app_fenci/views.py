from django.shortcuts import render, HttpResponse

# 首页
def fenci_index(request):
    return render(request, 'fenci_index.html')
