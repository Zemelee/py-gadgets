from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# 打开浏览器
browser = webdriver.Chrome()

# 进入淘宝手机网站
browser.get('https://m.taobao.com/')

# 等待页面加载
time.sleep(2)

# 定位搜索框
search_input = browser.find_element_by_xpath('//input[@type="search"]')

# 输入要搜索的商品名称
search_input.send_keys('手机')

# 点击搜索按钮
search_input.send_keys(Keys.ENTER)

# 等待页面加载
time.sleep(2)

# 定位所有商品链接
goods_links = browser.find_elements_by_xpath('//div[@class="items"]//a[@class="item-link"]')

# 依次进入每个商品页面
for link in goods_links:
    # 获取商品链接
    goods_link = link.get_attribute('href')
    # 进入商品页面
    browser.get(goods_link)
    # 等待页面加载
    time.sleep(2)
    # 定位商品型号、价格、颜色、参数等信息
    goods_info = {}
    goods_info['型号'] = browser.find_element_by_xpath('//div[@class="tb-detail-hd"]/h1/text()')
    goods_info['价格'] = browser.find_element_by_xpath('//strong[@class="price"]/text()')
    goods_info['颜色'] = browser.find_elements_by_xpath('//li[@class="sku-line"][1]//a[@class="item-sku-image"]')
    goods_info['参数'] = browser.find_elements_by_xpath('//ul[@class="attributes-list"]//li')
    # 打印商品信息
    print(goods_info)

# 关闭浏览器
browser.quit()
