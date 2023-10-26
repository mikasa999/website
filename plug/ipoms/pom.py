from selenium import webdriver
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import random
from fake_useragent import UserAgent
import requests
import json
import csv
import pandas
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Pom(object):

    def __init__(self):
        # 获取配置文件中的使用的搜索引擎的名字
        self.search_name = self.parse_config_txt()['search_name']
        print(f'初始化信息：使用的搜索引擎是[{self.search_name}]')

        # 从配置文件中获取要搜索的关键词
        self.search_keyword = self.parse_config_txt()['search_keyword']
        print(f'初始化信息：检测的关键词是“{self.search_keyword}”')

        # 获取配置文件中需要点击的总页数
        self.search_total_page = self.parse_config_txt()['search_total_page']
        print(f'初始化信息：本次共检测[{self.search_total_page}]页')

        # 统计爬完搜索的每一页总共获取的负面页面数量
        self.sensitive_page_num = 0

        # 检测保存搜索列表内容的文件是否存在，是否有内容，如果没有内容先写入列名
        with open(f'save/{self.search_name}_search_list.csv', 'a+', encoding='utf-8', newline='') as f:
            f.seek(0)  # 指针放到开头，否则a+模式指针在结尾，读不到文件内容
            con = f.read()
            if con == '':
                cons = csv.writer(f)
                cons.writerow(['搜索引擎', '搜索关键词', '列表页码', '列表行', '链接'])
                print('初始化信息：已为搜索内容文件创建新的字段')

        # 检测保存断点数据的文件是否存在，是否有内容，如果没有内容先写入列名
        with open(f'save/{self.search_name}_end_point.csv', 'a+', encoding='utf-8', newline='') as f:
            f.seek(0)  # 指针放到开头，否则a+模式指针在结尾，读不到文件内容
            con = f.read()
            if con == '':
                cons = csv.writer(f)
                cons.writerow(['搜索关键词', '断点链接', '断点页码'])
                print('初始化信息：已为断点记录文件创建新的字段')

        # 检测存储负面信息内容的的文件是否存在，是否有内容，如果没有内容先写入列名
        with open(f'save/{self.search_name}_sensitive_list.csv', 'a+', encoding='utf-8', newline='') as f:
            f.seek(0)  # 指针放到开头，否则a+模式指针在结尾，读不到文件内容
            con = f.read()
            if con == '':
                cons = csv.writer(f)
                cons.writerow(['搜索引擎', '搜索关键词', '列表页码', '列表行', '链接'])
                print('初始化信息：已为断点记录文件创建新的字段')


        # 获取要爬取的初始url，以及此url对应的页码
        self.search_url, self.search_page_num = self.parse_end_point()

        # 根据配置文件中的条件选择是否使用potion，无头模式、UA，proxy,是否加载图片等
        options = Options()
        if self.parse_config_txt()['proxy_ua'] == 'open':
            # print('开启->ip代理和随机UA')
            options.add_argument(f'--proxy-server={self.verify_proxy_ip()}')
            options.add_argument(f'--user-agent={UserAgent().random}')
        if self.parse_config_txt()['headless'] == 'open':
            print('初始化信息：无头模式已开启')
            options.add_argument('--headless')
        if self.parse_config_txt()['disable_images'] == 'open':
            prefs = {"profile.managed_default_content_settings.images": 2}
            print('初始化信息：禁止加载图片已开启')
            options.add_experimental_option("prefs", prefs)

        # 打开谷歌浏览器,配置文件中有个总开关，打开后才会传入options值
        if self.parse_config_txt()['options'] == 'open':
            # print('开启->options总开关')
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Chrome()

        print('------以上为初始化配置信息--------------', end="\n\n")

    # 打开搜索引擎，输入关键词，获取搜索后的列表页,PS:这个方法只适用于有分页页码的，不适用与知乎这种瀑布流加载以及需要登录的
    def run_search_engine(self):
        # # 测试：这里通过访问测试ip的网站来判断ip是否更换成功，通过js来返回useragent，判断ua是否随机使用成功
        # self.driver.get("https://ip.900cha.com/")
        # agent = self.driver.execute_script("return navigator.userAgent")
        # print(agent)
        # self.driver.close()

        # 根据search.json文件中的search_name 和 config.txt文件中的search_keyword来打开对应搜索引擎并进行搜索
        # 打开url
        self.driver.get(self.search_url)
        time.sleep(random.uniform(2, 5))

        # 如果是第一次抓取关键词则打开搜索引擎，输入关键词，按回车搜索
        if self.search_page_num == 1:
            # 从search json文件中获取选择元素的方法，用by.ID,BY.XPATH,BY.CLASS等等
            search_input_meta = self.parse_search_json()[self.search_name]['search_input_meta']
            # 从search json文件中获取选择选择的元素，query，input等
            search_input_element = self.parse_search_json()[self.search_name]['search_input_element']
            # getattr()通过这个方法，可以把字符串ID，变成常量ID。By.ID
            search_input_meta = getattr(By, search_input_meta)

            # 定位搜索框
            search_input = self.driver.find_element(search_input_meta, search_input_element)
            # 清空搜索框
            search_input.clear()
            # 输入关键词，这里加上延迟模拟手动输入
            for kw in self.search_keyword:
                search_input.send_keys(kw)
                time.sleep(random.uniform(0.2, 1))
            time.sleep(random.uniform(0.5, 1))
            # 按下回车搜索
            search_input.send_keys(Keys.ENTER)
            time.sleep(random.uniform(2, 5))

    # 依次点击搜索结果列表页中的每一条，获取列表的信息，在点击下一页继续，PS:这个方法只适用于有分页页码的，不适用与知乎这种瀑布流加载以及需要登录的
    def parse_search_list(self):
        # 从search.json中获取对用搜索引擎遍历列别的xpath
        search_list_xpath = self.parse_search_json()[self.search_name]['search_list_xpath']

        # 获得搜索结果列表的xpath对象
        search_list_elements = self.driver.find_elements(By.XPATH, search_list_xpath)

        # 先获取一下当前选项卡句柄下标
        main_window_handle = self.driver.current_window_handle

        # 遍历获取当前页通过xpath获取的列表总条目数
        total_list_num = 0
        for num in search_list_elements:
            total_list_num += 1
        # 如果检测到列表记录数量为0，则说明xpath错误，或者爬取的网站检测到爬虫，出现验证码或者未正确返回响应内容
        print(f'通知：当前页搜索结果共：[{total_list_num}]条')

        # 通过xpath获取了N组元素对象，再次遍历,开始逐个点击，并获取内容进行内容判断
        # 初始化当前列表中总记录数
        current_list_num = 1
        for el in search_list_elements:
            # 点击一次
            el.click()
            time.sleep(random.uniform(1, 2))
            # 获得所有标签句柄下标集合
            all_window_handles = self.driver.window_handles
            # 将选项卡句柄切换到新打开的选项卡
            self.driver.switch_to.window(all_window_handles[-1])

            # 用显式等待来判断是否已经获取到了需要的元素（好像也没什么用）
            # wait = WebDriverWait(self.driver, 8)
            # title_exists = wait.until(EC.presence_of_element_located((By.TAG_NAME, "title")))
            # html_exists = wait.until(EC.presence_of_element_located((By.TAG_NAME, "html")))

            time.sleep(random.uniform(5, 8))

            # 获取当前页面的title
            print(f'{current_list_num}/{total_list_num}/{self.search_page_num}:{self.driver.title}')

            # 获取当前页面中的html标签里的内容
            current_page_html = self.driver.find_elements(By.TAG_NAME, 'html')
            current_page_content = current_page_html[0].text

            # 如果获取的内容小于200个字符则说明返回不正确，直接跳过这个链接
            if len(current_page_content) < 100:
                print(f'Warning:本页页面内容未正常获取')

            self.parse_sensitive_json(page_content=current_page_content, current_list_num=current_list_num)

            # 保存点击进入后的网站内容，title，url，con等 ps:可以把这个文件打开写在最外层，就只需要打开关闭一次
            page_list_con = [self.search_name, self.search_keyword, self.search_page_num, current_list_num, self.driver.title, self.driver.current_url]
            with open(f'save/{self.search_name}_search_list.csv', 'a', encoding='utf-8', newline='') as f:
                csv_write = csv.writer(f)
                csv_write.writerow(page_list_con)

            # 关闭当前选项卡
            self.driver.close()

            # 切换回主选项卡
            self.driver.switch_to.window(main_window_handle)
            time.sleep(2)

            # 给当前遍历的第N条记录加1
            current_list_num += 1

        # 打印本搜索页中总共检测到了多少负面页面
        print(f'通知：此页面共检测到的负面数量:[{self.sensitive_page_num}]条')

        # 点击页面中的下一页，这里只针对有页码或者下一页选项的页面
        # xpath获取下一页，然后点击
        list_next_page = self.driver.find_element(By.XPATH, '(//a[contains(text(), "下一页")])[last()]')
        list_next_page.click()
        time.sleep(random.uniform(2, 5))

        self.search_page_num += 1

        # 每打开新的一页，就保存断点数据到对应文件
        self.save_end_point()

    # 解析end_point断点文件
    def parse_end_point(self):
        # 打开存储断点数据的文件，并进行判断
        with open(f'save/{self.search_name}_end_point.csv', 'r', encoding='utf-8', newline='') as f:
            fd = csv.reader(f)
            for row in fd:
                # 如果存储的关键词和配置文件中的搜索词一致，则返回断点存储的url和续爬页码
                if row[0] == self.search_keyword:
                    # 这里对不同的搜索引擎来构造对应的url+参数,这里有点复杂，但是放在search.json中也不行，后面想办法独立出去，或者简化。
                    search_url_main = self.parse_search_json()[self.search_name]['search_url'] + '/'
                    if self.search_name == 'sogou':
                        search_url = f"{search_url_main}web?query={row[0]}&page={row[2]}"
                    elif self.search_name == 'baidu':
                        search_url = f"{search_url_main}s?wd={row[0]}&pn={int(row[2])*10-10}"
                    elif self.search_name == 'haoso':
                        search_url = f"{search_url_main}s?q={row[0]}&pn={row[2]}"
                    elif self.search_name == 'bing':
                        search_url = f"{search_url_main}search?q={row[0]}&page={int(row[2])-1}1"
                    elif self.search_name == 'weixin':
                        search_url = f"{search_url_main}weixin?query={row[0]}&type=2&page={row[2]}"
                    elif self.search_name == 'tieba':
                        search_url = f"{search_url_main}f?kw={row[0]}&pn={int(row[2])*50-50}"
                    else:
                        print('错误：构造搜索引擎URL失败！')
                        break

                    search_page_num = int(row[2])
                    print(f'通知：检测到关键词”{self.search_keyword}“的爬取记录，本次搜索从第[{row[2]}页]开始')
                    return search_url, search_page_num
            else:
                search_url = self.parse_search_json()[self.search_name]['search_url']
                search_page_num = 1
                print(f'通知：关键词“{self.search_keyword}”未检测到爬取记录，将从第1页开始爬取')
                return search_url, search_page_num

    # 保存断点数据的三种情况：1、爬取结束后正常保存。2、每爬完一页保存一次
    def save_end_point(self):
        # 获取当前页码对应的url，并保存
        next_page_url = self.driver.current_url
        # 把当前搜索引擎名字，搜索词，当前url都写进csv文件中，下次爬取的时候读档判断
        con = [self.search_keyword, next_page_url, self.search_page_num]

        # 重组一个个新列表rows，把覆盖的内容添加后，重构一个大列表，整体增加到csv里面
        rows = []
        # 设置一个状态码，state_add_pattern 用1和2表示新增和覆盖
        state_add_pattern = 1

        # 断点记录进行新增或覆盖
        with open(f'save/{self.search_name}_end_point.csv', 'r', encoding='utf-8', newline='') as f:
            csv_read = csv.reader(f)
            # 把读取的一个一个小列表放到rows大列表里
            # 创建一个fd列表的副本rows
            for row in csv_read:
                if row[0] == self.search_keyword:
                    # row[:]相当用相同长度的列表覆盖row这个列表
                    row[:] = con
                    state_add_pattern = 2
                    # print(f'检测到关键词{self.search_keyword}已有搜索记录，进行覆盖重写')  # 测试：打印
                rows.append(row)

        if state_add_pattern == 1:  # 新增一行
            with open(f'save/{self.search_name}_end_point.csv', 'a', encoding='utf-8', newline='') as f:
                csv_write = csv.writer(f)
                csv_write.writerow(con)
                # print('增加了新的断点页码')
        else:  # 全部重写
            with open(f'save/{self.search_name}_end_point.csv', 'w', encoding='utf-8', newline='') as f:
                csv_write = csv.writer(f)
                csv_write.writerows(rows)
                # print('更新了新的断点页码')

    # 读取config配置文件，以字典的形式生成配置内容
    def parse_config_txt(self):
        # 创建一个字典，用于存储解析config文件的内容
        config_dict = dict()

        # 打开config文件
        with open('config.txt', 'r', encoding='utf-8') as f:
            # 逐行读取config文件中的内容,返回的是一个数组，每行的内容为一个元素，之后遍历每个元素。如果是f.read()会变成遍历成一个一个的字符
            config = f.readlines()
            # 开始遍历返回的数组
            for li in config:
                # 排除以下每一行中#号开头的字符，以及空行
                if li[0] != '#' and li != '\n':
                    try:
                        # index()来查找\n的位置，找不到会报错，所以用try和except。然后切割字符串，并放进字典里
                        str_num = li.index('\n')
                        li = li[0:str_num]
                        # 这里切割=只切一次，因为后面的链接里有很多等号，防止切割多次
                        config_dict[li.split('=', 1)[0]] = li.split('=', 1)[-1]
                    except:
                        config_dict[li.split('=', 1)[0]] = li.split('=', 1)[-1]
        return config_dict

    # 解析search.json文件，获取搜索引擎名称，url，xpath等信息
    def parse_search_json(self):
        # 打开search.json文件，获得IO流文件对象，用json.load把IO文件对象转化成python字典对象
        # 这里有个知识点 utf-8-sig,这个是一个utf-8的索引标记，可以用于写入csv文件，防止乱码，但是json不能有这个
        with open('search.json', encoding='utf-8') as f:
            # 获取字典对象，通过 object['name']['search_name']来使用内容
            search_info = json.load(f)
        return search_info

    # 解析sensitive.json存储敏感词数组的json文件，获取需要检测的敏感词，并进行判断存储。
    # page_content参数为传入页面内容，current_list_num传入当前页面第N条记录
    def parse_sensitive_json(self, page_content='1', current_list_num=1):
        # 设置临时统计变量，统计获取敏感词的次数，每预设的一组只要检测到即break退出，开始检测下一组预设敏感词列表
        counter_sensitive = 0
        # 统计sensitive_json中总共预设了多少组敏感词记录
        counter_sensitive_json_config_listnum = 0

        # 打开sensitive.json文件，获得IO文件对象，用json.load把IO文件对象转化成python字典对象
        with open('sensitive.json', encoding="utf-8") as f:
            # 将json文件内容转化为字典对象
            sensitive_info = json.load(f)
        # 遍历字典，获得字典中的多组一组预设的敏感词数据
        for key in sensitive_info:
            # 切割每一组预设敏感词到列表
            sensitive_list = sensitive_info[key].split(',')
            # 循环每一组列表
            for value in sensitive_list:
                # 如果检测到页面中有敏感词则counter_sensitive自增1
                if value in page_content:
                    counter_sensitive += 1
                    # print(f'注意：检测到敏感词：{value}，', end="")
                    break

            # 通过循环获得sensitive.json文件中总共预设了多少组敏感词记录
            counter_sensitive_json_config_listnum += 1

        # 如果统计的敏感词检测到的次数，和配置文件预设的敏感词组数量一致，则证明是负面信息，则保存
        if counter_sensitive == counter_sensitive_json_config_listnum:
            try:
                # 写入负面页面的相关信息到save文件中的sensitive_list.csv文件中
                with open(f"save/{self.search_name}_sensitive_list.csv", "a", encoding="utf-8", newline="") as f:
                    fd = csv.writer(f)
                    # 要写入文件的字段内容
                    sensitive_list = [self.search_name, self.search_keyword, self.search_page_num, current_list_num, self.driver.title, self.driver.current_url]
                    fd.writerow(sensitive_list)

                    # 当前搜索页面中检测到负面的页面数量自增
                    self.sensitive_page_num += 1

                    print(f'注意：检测到多个敏感词，已保存至对应文件')
            except:
                print('！检测到负面内容，但写入文件失败，请检查')


    # 处理代理ip的api，获得随机可用的ip地址,并对ip进行过滤，（判断是否可用，以及是http还是https类型）
    def parse_proxy_api(self):
        # 获取api链接
        url = self.parse_config_txt()['proxy_api']
        try:
            # 发送request请求，获取内容后，通过split \n切割字符串，返回一个列表，然后随机抽取列表中的一个元素
            response = requests.get(url)
            # 关闭打开的链接
            response.close()
            response = response.content.decode().split('\n')
            # 利用random.choice()函数随机获取列表中的一个元素ip地址
            response = random.choice(response)
            print(f'通知：当前IP：{response} | ', end="")
            return response
        except:
            print('获取代理ip失败，请检查代理api链接是否正确')

    # 这个方法用于检测parse_proxy_api解析出来的代理ip是否可用
    def verify_proxy_ip(self):
        # 这个是检测https的网站
        urls = 'https://ip.900cha.com/'
        # 这个是检测http的网站,这个可以不用验证，应为能打开https的都可以打开http
        url = 'http://httpbin.org/get'

        while True:
            # 获取parse_proxy_api()方法解析出来的ip
            response_ip = self.parse_proxy_api()

            # 测试：放一个错误的ip测试一下，之后删掉
            # response_ip = '12.256.2.35:8652'

            # 构造一个代理proxies字典
            proxies = {
                'http': f'http://{response_ip}',
                'https': f'http://{response_ip}'
            }
            # 构造UA参数所需的字典，这里用UserAgent().random可以随机生成一个UA
            headers = {
                'User-Agent': UserAgent().random
            }
            try:
                # 传入参数，打开url，获取响应
                response_urls = requests.get(urls, headers=headers, proxies=proxies, timeout=3)
                # 访问测试IP的https协议网站，根据状态码和返回的内容长度来判断是否访问正常
                if response_urls.status_code == 200 and len(response_urls.content) > 12000:
                    print('状态码=200,该IP可用')

                    # 测试：检测以下长度，看返回的内容是否正确，不过这里改成检测页面内容中显示的ip和设置的代理ip是否一致。这样更准确。
                    # print(f'获取内容长度：{len(response_urls.content)}')

                    # 关闭链接
                    response_urls.close()
                    return response_ip
                else:
                    # print('url可以成功，但状态码错误，1秒后获取新的ip重试')
                    print('该IP不可用，尝试更换IP')
                    # 关闭链接
                    response_urls.close()
                    time.sleep(1)
                    continue
            except:
                print('验证的ip打开url失败，1秒后获取新的ip重试')
                time.sleep(1)
                continue

    def main(self):
        # 先运行一下run_search_engine()，获得搜索页面
        self.run_search_engine()
        # 依次点击搜索结果，获取每条对应的相关内容，并进行判断相关操作
        self.parse_search_list()


if __name__ == '__main__':

    # 设置计数器变量counter_page，通过while每次结束前自增，获取当前已爬取的累计页数，和配置文件中的需要爬取的总页面数进行比较判断。
    counter_page = 1
    # 在运行方法里面循环，没页循环抓取，跑一次，然后关闭浏览器，更换ip重新接着断点页面抓取
    while True:
        try:
            # 每次循环重新实例化
            pom = Pom()
            pom.main()
            # 循环一次计数器变量+1
            counter_page += 1
            # 彻底关闭浏览器
            pom.driver.quit()
            time.sleep(3)
            # 如果counter_page大于了预设的最大爬取页面值，则退出，并将此搜索页的url保存，用于下次断点续爬
            if counter_page > int(pom.search_total_page):
                print('》抓取结束，已按配置文件设置的最大页面抓取量完成任务《')
                break
        except Exception as e:
            print(f'警告：发生错误,错误代码，跳出当前程序，重新开始', end="\n\n")
            pom = Pom()
            pom.driver.quit()
            continue
