from playwright.sync_api import sync_playwright
import time
import random

with sync_playwright() as playwright:
    browser = playwright.chromium.connect_over_cdp("http://localhost:9999")
    context = browser.contexts[0]

    page = context.new_page()

    page.goto("https://pharmacist.meituan.com/#/medicine/im")
    # page.goto("https://www.baidu.com/")
    time.sleep(random.uniform(1, 3))
    # 点击班次管理
    page.click('//label[text()=" 班次管理 "]')
    time.sleep(random.uniform(1, 2))

    # 统计刷新次数
    flush_num = 1
    # 总共获取到的班次
    work_num = 1
    # 时间列表
    time_list = [
        '17:00-18:00',
        '18:00-19:00',
        '19:00-20:00',
        '20:00-21:00',
        '21:00-22:00',
        '22:00-23:00',
        '23:00-24:00',
    ]
    # 刷新排班
    while True:
        page.click('//span[text()=" 刷新排班 "]')
        # 获取“可选”的xpath
        xpath_status_ok = '//label[text()=" 可选"]'
        # js动态加载的，需要等待一下页面加载完成
        time.sleep(random.uniform(1, 2))

        # xpath_status_ok = '//label[text()=" 满员"]'  # 测试
        # xpath_status_ok = '//*[contains(text(), "满员")]'  # 测试

        try:
            elements = page.query_selector_all(xpath_status_ok)
            # print(elements, end="")
            if not elements:
                raise Exception(f'第{flush_num}次刷新：没有获得数据')
        except Exception as e:
            print(e)
            flush_num += 1
            continue
        else:
            print(f'第{flush_num}次刷新：检测到了可选班次，检测时间是否符合要求')
            for element in elements:
                # 获取向上三级的td元素-》同辈的第一个td元素》span

                # xpath_time = f'{element}/../../../preceding-sibling::td//span' #错误示范
                # xpath_time = element.query_selector('../../../preceding-sibling::td//span') #错误示范

                # 暂时先关掉这个时间判断，测试成功了再打开
                right_time = element.query_selector('../../../preceding-sibling::td//span').text_content()
                print(f'当前可选班次对应的时间为：{right_time}', end="")
                if right_time in time_list:
                    print(f'*满足要求*')
                    try:
                        element.click()
                        print('点击“可选”成功')
                    except:
                        print('点击“可选”失败了')
                        continue
                    try:
                        page.click('//span[text()=" 确认选班 "]')
                        print('点击“确认选班”成功')
                    except:
                        print('点击“确认选班”失败了，本次抢班失败')
                        continue
                    else:
                        print(f'恭喜你抢到了：{right_time}的班次！，目前共获取了：{work_num}个班')
                        # 这里休眠一下，选班之后可能等一下可能需要js刷新等待加载
                        time.sleep(random.uniform(1, 2))
                        work_num += 1
                else:
                    print(f'时间不满足要求，跳过后继续')
            flush_num += 1
        finally:
            continue

        # time.sleep(random.randint(2, 3))
