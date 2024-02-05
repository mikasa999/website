from django.shortcuts import render, HttpResponse

#首页
def crm_index(request):
    return render(request, 'crm_index.html')

