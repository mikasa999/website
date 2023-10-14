import random
from playwright.sync_api import sync_playwright
from time import sleep

class tanji_customer_export():

    def __init__(self):
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch_persistent_context(
            # 指定本机用户缓存地址
            user_data_dir=f"F:\playwright_data\cy",
            # 接收下载事件
            accept_downloads=True,
            # 设置 GUI 模式
            headless=False,
            args=["--start-maximized"],
            no_viewport=True,
            bypass_csp=True,
            slow_mo=2000,
            channel="msedge",
        )

        self.browser = browser
        self.page = browser.pages[0]

    def get_xp_list(self):
        #打开登录页面
        self.page.goto('https://user.tungee.com/home')
        # page.goto('https://www.baidu.com/')
        #这里先扫码登录
        sleep(3)
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
        self.page.click('//li[text()="械品-招商-1.01"]')
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

        #//tbody[@class="ant-table-tbody"]/tr/td[2]
        #//li[@title="下一页"]
        #开始获取页面中的内容

    def click_next_page(self):
        self.page.click('//li[@title="下一页"]')

    def get_page_content(self):
        xpath = '//div[@class="ant-table-scroll"]//tbody[@class="ant-table-tbody"]//tr'
        elements = self.page.query_selector_all(xpath)
        # print(f'总共获取元素：{elements.count}')
        for element in elements:
            phone = element.query_selector('//td[2]').text_content()
            company = element.query_selector('//td[3]').text_content()
            customer = element.query_selector('//td[4]').text_content()
            tel_status = element.query_selector('//td[8]').text_content()
            tel_result = element.query_selector('//td[9]').text_content()
            tel_longtime = element.query_selector('//td[11]').text_content()

            # print(f'{phone};{company};{customer};{tel_status};{tel_result};{tel_longtime}')
            # return phone, company, customer, tel_status, tel_result, tel_longtime
            # models.tanji_customer_export.objects.create(
            #     phone=phone,
            #     company=company,
            #     customer=customer,
            #     tel_status=tel_status,
            #     tel_result=tel_result,
            #     tel_longtime=tel_longtime,
            # )
            print('本行数据已写入数据库')


    def run(self):
        self.get_xp_list()
        page_num = 1
        while True:
            print(f'=======当前是第{page_num}页==========')
            self.get_page_content()
            self.click_next_page()
            sleep(random.uniform(3, 7))
            page_num += 1
            if page_num > 2:
                break
        self.browser.close()

# if __name__ == '__main__':
#     customer = tanji_customer_export()
#     customer.run()
