# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import csv

url = 'https://movie.douban.com/top250'

# 设置请求头
header = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

with open('../practice/豆瓣电影top250.csv', 'w', encoding='utf-8', newline='') as file:
    # 给csv文件添加表头
    csvWriter = csv.DictWriter(file,
                               fieldnames=['电影名称', '电影简介', '电影类型', '国家', '上映年份', '评分', '评价人数',
                                           '封面'])
    csvWriter.writeheader()
    a = 0
    for start in range(0, 226, 25):

        print("正在爬取第{}页...".format(int(start / 25 + 1)))
        html = requests.get(url=url, params={'start': start}, headers=header)
        soup = BeautifulSoup(html.text, "html.parser")
        htm = etree.HTML(html.text)
        # 每一页25部电影
        for num in range(1, 26):

            # 电影名称
            film_name = soup.select(
                "#content > div > div.article > ol > li:nth-child({}) > div > div.info > div.hd > a > span".format(
                    num))[0].get_text()
            # 图片链接
            pic_link = soup.select(
                "#content > div > div.article > ol > li:nth-child({}) > div > div.pic > a > img".format(num))[0]['src']
            # 电影评分
            film_score = soup.select(
                "#content > div > div.article > ol > li:nth-child({}) > div > div.info > div.bd > div > span.rating_num".format(
                    num))[0].get_text()
            # 评价人数
            film_eval = soup.select(
                "#content > div > div.article > ol > li:nth-child({}) > div > div.info > div.bd > div > span:nth-child(4)".format(
                    num))[0].get_text()
            try:
                # 简介
                film_intro = soup.select(
                    "#content > div > div.article > ol > li:nth-child({}) > div > div.info > div.bd > p.quote > span".format(
                        num))[0].get_text()
            except:
                film_intro = '暂无简介'

            try:
                # 年份/国家/类型
                film_type_text = \
                    htm.xpath("//*[@id='content']/div/div[1]/ol/li[{}]/div/div[2]/div[2]/p[1]/text()[2]".format(num))[0]
                pattern = '(\d{4})\s/\s(.*?)\s/\s(.*)'
                film = re.findall(pattern=pattern, string=film_type_text)[0]
                film_year = film[0]
                film_country = film[1]
                film_type = film[2]
            except:
                film_year = "暂无"
                film_country = "暂无"
                film_type = "暂无"

            dict = {
                "电影名称": film_name,
                "电影简介": film_intro,
                "电影类型": film_type,
                "国家": film_country,
                "上映年份": film_year,
                "评分": film_score,
                "评价人数": film_eval,
                "封面": pic_link
            }

            csvWriter.writerow(dict)

print("爬取完成")
