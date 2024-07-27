import requests
from lxml import etree
import csv
import random
import time

header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.88,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'cookie': 'shshshfpa=fe23a925-42fb-bb5d-ee94-0e60189fb078-1663154100; shshshfpb=j9iW0pAOpnqH8ORHSn2bVtw; unpl=JF8EALxnNSttWUJcB04LHRBCHAhdW1tcSEcAOmMGUFtfTwEBHgdMRRJ7XlVdXhRLFx9sZxRVVVNJUQ4eBCsSEXtdVV9fD0oeBm5vNWRVW0oGDUwHEhZ-SzNcFw91KxYCEQRTFm1bS2QEKwIcFhNDWFJdXgtNEQpvYw1WW1hCVwMcMhoiEENZZG5tDUsWAm5vAlVaWXtVNRkDGhcUSlpVXVo4AHkCImcCUF5QTlIGGAEdFBlLWVxcWwhCFAVoVwRkXg; areaId=22; ipLoc-djd=22-1930-0-0; PCSYCityID=CN_510000_510100_0; __jdv=122270672|www.baidu.com|t_1003608409_|tuiguang|0893d873cfd847e2a2d525765d544ff3|1668994514611; TrackID=1MKxLRzR25daGriArGGjXc7bbt5bgQbqdANqnEnyKuGFe2tqRCtNwmV-zk8qn0wcL315R-8v7h6sVN4ZwwcD9qGwlL-u6rgJj_IdFzXdfGU6ZuEyq1zQP3x6Xgoinx3Pa; thor=1C6E5E19E85D36AB91EE08B716F3538BA9C585A7FAC632D7D8554D29D95E7F5241D9BC1AC3FECF3D18DAC18F6CF3490D906E1E24FF7C33F8BBBFD3BB1A351B0A9EE4831F4983324BC7359109B3B5DB80B38A61E118BBA08C9CDA9D95115D2E5D9681FB4963FCBA2BD0CE2DCAD4A2094DC3211D092465433632C1F6B345C21A2FC41508797FD699F6EA2528160860721EFC2DDCCF96BAC1428F5913E5782210AC; pinId=yATIe1TewGKWNB7jvYkC2A; pin=jd_iETKXLxguyEA; unick=jd_iETKXLxguyEA; ceshi3.com=000; _tp=5scZ0XGM7LBVpxiRbWggPA%3D%3D; _pst=jd_iETKXLxguyEA; jsavif=0; jsavif=0; __jda=122270672.16529472227781593718276.1652947222.1665226336.1668994494.8; __jdb=122270672.6.16529472227781593718276|8.1668994494; __jdc=122270672; qrsc=1; rkv=1.0; shshshfp=2fe3c14e67139f4ca3998a211710de16; shshshsID=15c7fbb5e473bc1a3727d04c5e201f5c_3_1668994561225',
    'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52',
}


# 获取列表目标数据的函数
def getLi(li_list):
    for li in li_list:
        # 商品名称
        name = li.xpath(".//div[@class='p-name p-name-type-2']/a/em/text()")
        gift_name = "".join(name)
        print("商品名称：", gift_name)

        # 商品价格
        price = "￥" + li.xpath(".//div[@class='p-price']/strong/i/text()")[0]
        print("商品价格：", price)

        # 店铺名称
        store_name = li.xpath(".//div[@class='p-shop']/span/a/text()")[0]
        print("店铺名称:", store_name)


        # 商品编号
        sku = li.xpath("@data-sku")

        # 商品其他数据细节
        details = requests.get('https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}'.
                               format(sku[0]), headers=header).json()
        # 商品评论量
        comments = details['CommentsCount'][0]['CommentCountStr']
        print("商品评论量:", comments)

        # 发货地
        store_place = li.xpath(".//div[@class='p-stock hide']/@data-province")[0]
        print("发货地:", store_place)

        # 商品链接
        link = li.xpath(".//div[@class='p-img']/a/@href")
        gift_link = "https:" + link[0]
        print("商品链接:", gift_link)

        # 店铺链接
        store_link = li.xpath(".//div[@class='p-shop']/span/a/@href")[0]
        store_link = "https:" + store_link
        print("店铺链接:", store_link)

        # 图片链接
        link = li.xpath(".//div[@class='p-img']/a/img/@data-lazy-img")
        pic_link = "https:" + link[0]
        print("图片链接:", pic_link, "\n")
        dict = {
            "商品名称": gift_name,
            "商品价格": price,
            "店铺名称": store_name,
            "商品评论量": comments,
            "发货地": store_place,
            "商品链接": gift_link,
            "店铺链接": store_link,
            "图片链接": pic_link,
        }
        csvWriter.writerow(dict)


with open('京东.csv', 'w', encoding='utf-8', newline='') as file:
    # 给csv文件添加表头
    csvWriter = csv.DictWriter(file, fieldnames=['商品名称', '商品价格', '店铺名称', '商品评论量', '发货地', '商品链接', '店铺链接', '图片链接'])
    csvWriter.writeheader()
    # 爬取1-16页
    for page in range(1, 17):
        # 随机睡眠1-4秒，防反爬机制
        time.sleep(random.randint(1, 4))
        print("------正在爬取第{}页------".format(page))
        # 拼接需要爬取的链接
        url = 'https://search.jd.com/Search?keyword=%E8%9C%80%E7%BB%A3&enc=utf-8&wq=%E8%9C%80%E7%BB%A3' \
              '&pvid=73e1e387d6514ed59c14829d065c8ace&page={}'.format(page)
        response = requests.get(url=url, headers=header)
        print(response)  # 状态码
        html = response.text
        # 网页源代码
        htm = etree.HTML(html)
        # 源代码里的商品列表
        li_list = htm.xpath("//*[@id='J_goodsList']/ul/li")
        # 获取列表详情
        dict = getLi(li_list)
