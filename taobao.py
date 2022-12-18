import time
from datetime import datetime

import tool

PURCHASE_TIME = "2022-12-18 13:22:40"
TAOBAO_MAIN_PAGE = "https://www.taobao.com"
TAOBAO_CART_PAGE = "https://cart.taobao.com/cart.htm"
NUM_OF_PRO = 1


def init():
    # the prerequisite for the purchase
    tool.get_chrome_driver()
    tool.taobao_login_operate(TAOBAO_MAIN_PAGE)
    # wait for a while
    buy_time = datetime.strptime(PURCHASE_TIME, '%Y-%m-%d %H:%M:%S')
    while (buy_time - datetime.now()).seconds > 120:
        tool.flush_page(TAOBAO_CART_PAGE)
        time.sleep(60)


def purchase():
    tool.choose_item(TAOBAO_CART_PAGE, NUM_OF_PRO)
    buy_time = datetime.strptime(PURCHASE_TIME, '%Y-%m-%d %H:%M:%S')
    # purchasing
    retrytime = 0
    while True:
        if datetime.now() > buy_time:
            if retrytime > 100:
                print("失败了，寄")
                break
            print("start purchasing")
            suc = tool.purchase_item()
            if suc:
                print("成功，但是需要自己去付款")
                break
            retrytime = retrytime + 1


if __name__ == '__main__':
    init()
    purchase()
