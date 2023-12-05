from django.shortcuts import render, HttpResponse

def yaoshi_index(request):
    #药师抢班首页
    return render(request, 'yaoshi_index.html')