import random
from playwright.sync_api import sync_playwright
from time import sleep
import pymysql
import asyncio

class tanji_customer_export():

    def __init__(self, use_time, check_name, talk_content):
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch_persistent_context(
            # 指定本机用户缓存地址
            user_data_dir=f"F:\playwright_data\cy",
            # 接收下载事件
            accept_downloads=True,
            # 设置 GUI 模式
            headless=False,
            # 全屏
            args=["--start-maximized"],
            no_viewport=True,

            bypass_csp=True,
            slow_mo=2000,
            channel="msedge",
        )

        self.use_time = use_time
        self.browser = browser
        self.page = browser.pages[0]
        self.conn = self.connect_sql()
        self.cursor = self.conn.cursor()
        self.page_num = 1
        self.check_name = check_name
        self.talk_content = talk_content

    def get_result_filter(self):
        if self.check_name == '有效':
            print('过滤信息选择了除”其他“外的所有选项')
            self.page.click('//span/div/span[text()="AI推荐"]')
            sleep(random.randint(1, 2))
            self.page.click('//span/div/span[text()="加微信/发资料/面谈"]')
            sleep(random.randint(1, 2))
            self.page.click('//span/div/span[text()="同意邀约"]')
            sleep(random.randint(1, 2))
            self.page.click('//span/div/span[text()="价格"]')
            sleep(random.randint(1, 2))
            self.page.click('//span/div/span[text()="公司/地址/案例"]')
            sleep(random.randint(1, 2))
            self.page.click('//span/div/span[text()="在忙/考虑"]')
            sleep(random.randint(1, 2))
            self.page.click('//span/div/span[text()="有合作/非kp"]')
            sleep(random.randint(1, 2))
            self.page.click('//span/div/span[text()="知识库＞3"]')
            sleep(random.randint(1, 2))
            self.page.click('//span/div/span[text()="通话＞60s"]')
            sleep(random.randint(1, 2))
            self.page.click('//span/div/span[text()="拒绝"]')
            sleep(random.randint(1, 2))
        elif self.check_name == '其他':
            print('过滤信息选择了：其他')
            self.page.click('//span/div/span[text()="其他"]')
            sleep(random.randint(1, 2))
        elif self.check_name == '全部':
            print('选择了全部信息')
            sleep(random.randint(1, 2))
        elif self.check_name == '接通':
            print('选择了接通的电话')
            self.page.click('//div/span[text()="接通"]')
            sleep(random.randint(1, 2))
        else:
            print('未过滤任何信息')

    def get_xp_list_huashu(self):
        #打开登录页面
        self.page.goto('https://user.tungee.com/home')
        # page.goto('https://www.baidu.com/')
        #这里先扫码登录
        sleep(self.use_time)
        #定位到企业中心的“探迹智能呼叫”点击进入机器人页面
        self.page.click('//span[text()="探迹智能呼叫"]')
        sleep(random.uniform(1, 2))
        #点击“通话明细”
        self.page.click('//span[text()="通话明细"]')
        sleep(random.uniform(1, 2))
        #点击“任务查询”
        self.page.click('//a[text()="任务查询"]')
        sleep(random.uniform(1, 2))
        #点击下拉框中的“话术查询”
        self.page.click('//li[text()="话术查询"]')
        sleep(random.uniform(1, 2))
        #点击选择话术的div
        self.page.click('//*[@id="app-content"]/div/div/div/div/div[1]/table/tbody/tr[1]/td/span/input')
        sleep(random.uniform(1, 2))
        #选择"械品-招商-1.01"的话术
        self.page.click(f'//li[text()="{self.talk_content}"]')
        sleep(random.uniform(1, 2))
        #选择“第1版”
        self.page.click('//li[text()="第1版"]')
        sleep(random.uniform(1, 2))
        #点击下面“10条/页”
        self.page.click('//div[text()="10 条/页"]')
        sleep(random.uniform(1, 2))
        #选择50条/页
        self.page.click('//li[text()="50 条/页"]')
        sleep(random.uniform(1, 2))

        # 点击外呼结果的选项，进行筛选过滤，减少爬取数量。
        self.get_result_filter()


        #//tbody[@class="ant-table-tbody"]/tr/td[2]
        #//li[@title="下一页"]
        #开始获取页面中的内容
    def get_xp_list_renwu(self):
        #打开登录页面
        self.page.goto('https://user.tungee.com/home')
        # page.goto('https://www.baidu.com/')
        #这里先扫码登录
        sleep(self.use_time)
        #定位到企业中心的“探迹智能呼叫”点击进入机器人页面
        self.page.click('//span[text()="探迹智能呼叫"]')
        sleep(random.uniform(1, 2))
        #点击“通话明细”
        self.page.click('//span[text()="通话明细"]')
        sleep(random.uniform(1, 2))
        #点击“任务查询”
        self.page.click('//a[text()="任务查询"]')
        sleep(random.uniform(1, 2))
        #点击下拉框中的“话术查询”
        self.page.click('//li[text()="任务查询"]')
        sleep(random.uniform(1, 2))
        #点击选择话术的div
        self.page.click('//*[@id="app-content"]/div/div/div/div/div[1]/table/tbody/tr[1]/td/div/div/div/div[1]')
        sleep(random.uniform(1, 2))
        #选择"械品-招商-1.01"的话术
        self.page.click(f'//li[text()="{self.talk_content}"]')
        sleep(random.uniform(1, 2))
        #点击下面“10条/页”
        self.page.click('//div[text()="10 条/页"]')
        sleep(random.uniform(1, 2))
        #选择50条/页
        self.page.click('//li[text()="50 条/页"]')
        sleep(random.uniform(1, 2))

        # 点击外呼结果的选项，进行筛选过滤，减少爬取数量。
        self.get_result_filter()


        #//tbody[@class="ant-table-tbody"]/tr/td[2]
        #//li[@title="下一页"]
        #开始获取页面中的内容

    def click_next_page(self):
        self.page.click('//li[@title="下一页"]')
        sleep(random.uniform(5, 10))

    # 链接数据库
    def connect_sql(self):
        try:
            conn = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='root',
                db='allen',
                charset='utf8mb4'
            )
            print('数据库连接成功')
        except Exception as e:
            print(e)
        else:
            return conn

    def get_page_content(self):
        xpath = '//div[@class="ant-table-scroll"]//tbody[@class="ant-table-tbody"]//tr'
        elements = self.page.query_selector_all(xpath)
        # print(f'总共获取元素：{elements.count}')
        # 遍历并获取电话，公司名称等信息
        if elements == '':
            print('未加载到信息，这里等待加载30s')
            sleep(30)
        list_num = 1
        for element in elements:
            phone = element.query_selector('//td[2]').text_content()
            company = element.query_selector('//td[3]').text_content()
            customer = element.query_selector('//td[4]').text_content()
            tel_status = element.query_selector('//td[8]').text_content()
            tel_result = element.query_selector('//td[9]').text_content()
            tel_longtime = element.query_selector('//td[11]').text_content()

            # 把数据插入数据库
            sql = "insert into app_tanji_customer_list(phone, company, customer,tel_status, tel_result, tel_longtime) values (%s,%s,%s,%s,%s,%s)"
            values = (phone, company, customer, tel_status, tel_result, tel_longtime)
            try:
                self.cursor.execute(sql, values)
                self.conn.commit()
                print(f'{list_num}/{self.page_num}插入成功！电话：{phone}，联系人：{customer}')
                list_num += 1
            except Exception as e:
                print(e)


    def run(self):
        self.get_xp_list_renwu()
        while True:
            print(f'=======当前是第{self.page_num}页==========')
            self.get_page_content()
            self.click_next_page()
            sleep(random.randint(2, 3))
            self.page_num += 1
            if self.page_num > 5000:
                break
        self.browser.close()
        self.conn.close()

if __name__ == '__main__':
    tce = tanji_customer_export(3, '全部', '械品-23100101')
    tce.run()
