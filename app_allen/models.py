from django.db import models

class pom_run_config(models.Model):
    pom_create_date = models.DateTimeField(verbose_name='创建日期')
    pom_scan_platform_choices = (
        ("baidu", "百度"),
        ("sogou", "搜狗"),
        ("haoso", "好搜"),
        ("bing", "必应"),
        ("weixin", "微信公众号"),
        ("tieba", "贴吧"),
        ("weibo", "微博"),
        ("zhihu", "知乎"),
    )
    pom_scan_platform = models.CharField(verbose_name='扫描平台', max_length=10, choices=pom_scan_platform_choices)
    pom_scan_page_num_choices = (
        (3, "3"),
        (5, "5"),
        (10, "10"),
        (15, "15"),
        (20, "20"),
        (25, "25"),
        (50, "50"),
        (100, "100"),
    )
    pom_scan_page_num = models.SmallIntegerField(verbose_name='检测页数', choices=pom_scan_page_num_choices)
    pom_scan_keywords = models.CharField(verbose_name='检索关键词', max_length=3000)
    pom_headless = models.CharField(verbose_name='无头模式', max_length=4)
    pom_stop_load_pic = models.CharField(verbose_name='禁止加载图片', max_length=4)
    pom_proxy = models.CharField(verbose_name='使用代理', max_length=4)
    pom_ua = models.CharField(verbose_name='动态UA', max_length=4)
    pom_login_pattern = models.CharField(verbose_name='登录模式', max_length=4)
    pom_proxy_api = models.CharField(verbose_name='PROXY API', max_length=300, null=True, blank=True)
    pom_cookies = models.CharField(verbose_name='COOKIES', max_length=300, null=True, blank=True)
    pom_token = models.CharField(verbose_name='TOKEN', max_length=300, null=True, blank=True)
    pom_username = models.CharField(verbose_name='用户名', max_length=16, null=True, blank=True)
    pom_password = models.CharField(verbose_name='密码', max_length=32, null=True, blank=True)

class tanji_customer_export(models.Model):
    phone = models.CharField(verbose_name='联系电话', max_length=15)
    company = models.CharField(verbose_name='公司名称', max_length=50)
    customer = models.CharField(verbose_name='客户姓名', max_length=50)
    tel_status = models.CharField(verbose_name='电话状态', max_length=15)
    tel_result = models.CharField(verbose_name='拨号结果', max_length=15)
    tel_longtime = models.CharField(verbose_name='通话时常', max_length=10)
