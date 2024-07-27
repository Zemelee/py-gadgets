import requests  # 爬虫专属第三方库，可以获取网页源代码
import re  # 正则表达式库，用于提取源码中的目标文本
import pprint  # 格式化输出，（解释为了输出更美观不混乱）
import json  # json用于将python字典格式转化为json格式
import csv  # 没学过，我猜应该和excel差不多吧，用来存储数据
import time  # 可以是程序暂停
import random  # 获取随机数

from bs4 import BeautifulSoup



# 爬取1-6页
print("------正在爬取------")
# 淘宝搜索 蜀绣 后的链接
url = f'https://s.taobao.com/search?fromTmallRedirect=true&q=%E8%8C%B6%E5%8F%B6&spm=875.7931836%2FB.a2227oh.d100&tab=mall'
# 请求头，将此程序伪装成浏览器，防止淘宝反爬机制
header = {
    'Host': 's.taobao.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': 'cna=lcxHHNWIO3UCAbaGRWNGSsrr; tracknick=%5Cu4E0D%5Cu66FE%5Cu76F8%5Cu9047%5CuFF01005009; _cc_=UIHiLt3xSw%3D%3D; thw=cn; miid=128231032120570281; t=3380672d980f56f4ebbc29bb603d4c5c; _tb_token_=e9ee34da7e1ee; _m_h5_tk=93293a29b8a61ee1a0dc24f833bafba2_1693923562557; _m_h5_tk_enc=e10b27db36c9ed14cde6f728a20c5435; xlly_s=1; tfstk=doq2HjZrUiI2w3ggS2oaLrNG5rnxfDCC0lGsIR2ihjcmGRDib7V1HjwGM5rZZRUfHV1vQKEzThtfMZeMbciGO6sCA-BxXcfQJDsQHs9obg1CAMwAojRBu619VnGFEph9gtmFubwV96S22vpj_-cyb-Ernq8Ynb-MjuzruO7J6YjdClU2sFumeYlCUTJm-GIP.; l=fBPBcAerT7O9met2BOfwPurza77OSIRAguPzaNbMi9fPO3fp5AxfW1Tk0D89C3GVF62DR3rNfwdWBeYBqCcGSQLy2j-la_kmnm9SIEf..; isg=BHp6kzOWygK1vEF1IJ7143J0y6CcK_4FZ2zpG4RzAo3YdxqxbLv4FdKNxwOrZ3ad',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers',
}
time.sleep(random.randint(1, 4))
# 获取网页源码，同时附带请求头
response = requests.get(url=url, headers=header).text
soup = BeautifulSoup(response, "html.parser")
print(soup)
a_tags = soup.find_all('a', class_='Card--doubleCardWrapperMall--uPmo5Bz')
for a in a_tags:
    href = a.get('href')
    print(f'Found URL: {href}')
print("爬取完成")
