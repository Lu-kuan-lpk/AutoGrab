import time

from selenium import webdriver
import os

MAX_RETRY = 10
driver = 0

def get_chrome_driver():
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument('--disable-blink-features=AutomationControlled')
    chromedriver = os.path.join(os.getcwd(), 'chromedriver_windows')
    global driver
    driver = webdriver.Chrome(chromedriver, options=option)
    driver.maximize_window()


def taobao_login_operate(location):
    driver.get(location)
    login_suc = False
    retry_time = 0
    while not login_suc and retry_time < MAX_RETRY:
        try:
            if driver.find_element_by_link_text("亲，请登录"):
                driver.find_element_by_link_text("亲，请登录").click()
                print("使用手机淘宝扫描屏幕上的二维码登录...,此页面停留20s")
                driver.find_element_by_class_name("icon-qrcode").click()
                time.sleep(20)
        except:
            print("已登录，开始执行跳转...")
            global current_retry_login_times
            login_suc = True
            retry_time = retry_time+1

def flush_page(location):
    driver.get(location)

def choose_item(location,num):
    # 打开购物车
    driver.get(location)
    time.sleep(1)
    products = driver.find_elements_by_xpath("//div[@class='td-inner']//div[@class='cart-checkbox ']")[0:num]
    for pro in products:
        pro.click()
    print("已经选中购物车部分商品")

def purchase_item():
    try:
        # 点击结算按钮
        if driver.find_element_by_id("J_Go"):
            driver.find_element_by_id("J_Go").click()
            print("已经点击结算按钮...")
            click_submit_times = 0
            while True:
                try:
                    if click_submit_times < 10:
                        driver.find_element_by_link_text('提交订单').click()
                        print("已经点击提交订单按钮")
                        submit_succ = True
                        break
                    else:
                        print("提交订单失败...")
                except Exception as ee:
                    # print(ee)
                    print("没发现提交订单按钮，可能页面还没加载出来，重试...")
                    click_submit_times = click_submit_times + 1
                    time.sleep(0.1)
    except Exception as e:
        print(e)
        print("不好，挂了，提交订单失败了...")
    return submit_succ