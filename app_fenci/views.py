from django.shortcuts import render, HttpResponse

# 首页
def fenci_index(request):
    return render(request, 'fenci_index.html')

# 主词根添加
def fenci_zcg(request):
    return render(request, 'fenci_zcg.html')

# 清洗词添加
def fenci_qxc(request):
    return render(request, 'fenci_qxc.html')

# 非业务词添加
def fenci_fywc(request):
    return render(request, 'fenci_fywc.html')

# 业务词添加
def fenci_ywc(request):
    return render(request, 'fenci_ywc.html')

# 分词词性添加
def fenci_fc(request):
    return render(request, 'fenci_fc.html')

