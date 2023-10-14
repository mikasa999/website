from django.db import models

class customer_list(models.Model):
    phone = models.CharField(verbose_name='联系电话', max_length=15)
    company = models.CharField(verbose_name='公司名称', max_length=50)
    customer = models.CharField(verbose_name='客户姓名', max_length=50)
    tel_status = models.CharField(verbose_name='电话状态', max_length=15)
    tel_result = models.CharField(verbose_name='拨号结果', max_length=15)
    tel_longtime = models.CharField(verbose_name='通话时常', max_length=10)
