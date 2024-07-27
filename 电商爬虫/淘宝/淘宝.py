import requests  # 爬虫专属第三方库，可以获取网页源代码
import re  # 正则表达式库，用于提取源码中的目标文本
import pprint  # 格式化输出，（解释为了输出更美观不混乱）
import json  # json用于将python字典格式转化为json格式
import csv  # 没学过，我猜应该和excel差不多吧，用来存储数据
import time  # 可以是程序暂停
import random  # 获取随机数

#以写入数据的方式（w）打开tabbao.csv文件（与之相关的还有读取数据方式打开（r））
with open('taobao.csv', 'w', encoding='utf-8', newline='') as file:
    #给csv文件添加表头
    csvWriter = csv.DictWriter(file, fieldnames=['标题', '价格', '店铺', '销量', '地点', '商品详情页', '店铺链接', '图片链接'])
    csvWriter.writeheader()

    # 爬取1-6页
    for page in range(0, 7):
        print("------正在爬取第{}页------".format(page + 1))
        #淘宝搜索 蜀绣 后的链接
        url = f'https://s.taobao.com/search?q=%E8%9C%80%E7%BB%A3&suggest=history_1&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.jianhua.201856-taobao-item.2&ie=utf8&initiative_id=tbindexz_20170306&_input_charset=utf-8&wq=&suggest_query=&source=suggest&bcoffset=1&ntoffset=1&p4ppushleft=2%2C48&s={page * 44}'
        #请求头，将此程序伪装成浏览器，防止淘宝反爬机制
        header = {
            'Host': 's.taobao.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cookie': '_samesite_flag_=true; cookie2=146133699947efe7828bb5ddc9a6aa1c; t=b5edb7fc90d3ebea799c9331aa306925; _tb_token_=e7e6661e3b337; tfstk=ccnVBycP_nK2XWozAuqZYM8ETBEAZa4g8gyToCfk20xpaJaliK1TEdDbUJBPsrf..; cna=i/IAHGlH1EUCAbaVaT/pIiIH; isg=BHV1ITUlek5nl57yY8H_vOD-h_Ev8ikEr14EO_eaV-w7zpTAv0A01MtMHBJ4lUG8; l=eBg8pTagTc29GH9EBOfZ-urza77thIObYuPzaNbMiOCPOhCp5K1OW6za8WL9Cn1VHsMkR3oXCczJBr81Yydq0-Y3L3k_J_fs3dC..; xlly_s=1; sgcookie=E100LoV37ZcFjHqWbaiiew7xU%2BrCLjSr%2BrMsELtcb%2B23tcIHeqjvUlJhSOscZUZrGxyAibSFC6mC5xnLXWyPVU5SZuo5wPPZsLEQeVkF8%2Bm%2BCfg%3D; unb=3210834116; uc1=cookie21=URm48syIYn73&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&cookie14=UoeyBrL5pwTLBw%3D%3D&existShop=false&pas=0; uc3=nk2=0XngSmsSKpj0wwOWSbsC3w%3D%3D&id2=UNJQ7f%2B6tY4GWw%3D%3D&vt3=F8dCvjT9nobyg970siE%3D&lg2=UtASsssmOIJ0bQ%3D%3D; csg=14796fea; lgc=%5Cu4E0D%5Cu66FE%5Cu76F8%5Cu9047%5CuFF01005009; cancelledSubSites=empty; cookie17=UNJQ7f%2B6tY4GWw%3D%3D; dnk=bla_ck_sugar; skt=97d3f106408515db; existShop=MTY2ODk0MDk4OQ%3D%3D; uc4=nk4=0%4000HLUIMKZA3ZHQYXvMgRDFAsR%2BN3w54CLfcP&id4=0%40UgXXlMq5mQaj9pTkkCJPMLG2q3lv; tracknick=%5Cu4E0D%5Cu66FE%5Cu76F8%5Cu9047%5CuFF01005009; _cc_=UtASsssmfA%3D%3D; _l_g_=Ug%3D%3D; sg=962; _nk_=%5Cu4E0D%5Cu66FE%5Cu76F8%5Cu9047%5CuFF01005009; cookie1=AC5Vp9PTAXaEAtfGbDTJjBuDrCJDOuyuo6Qxie%2B%2Bgbc%3D; enc=pRzVNbKJtlbI64jSFbUWgtT7o4Sc33MR8aSrzlpxgmotibPpF8C6vFWV5HJ6GX4fNGc7a4sEV0WUVNBSuv2psA%3D%3D; JSESSIONID=4AC872E11B9CE0E75A6CF007351B103F',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers',
        }

        # 随机睡眠1-4秒，防反爬机制
        time.sleep(random.randint(1, 4))
        # 获取网页源码，同时附带请求头
        response = requests.get(url=url, headers=header)
        # print(response.text)
        # 正则表达式匹配商品内容，此时商品详情在 html_data 里，其为字典格式
        html_data = re.findall('g_page_config = (.*);', response.text)[0]
        # 将字典转换成json
        json_data = json.loads(html_data)
        # 格式化输出json
        pprint.pprint(json_data)
        #提取商品详情，将需要的数据提取出来
        data = json_data['mods']['itemlist']['data']['auctions']
        # 遍历商品内容，获取关键表项
        for index in data:
            dict = {
                '标题': index['raw_title'],
                '价格': index['view_price'],
                '店铺': index['nick'],
                '销量': index['view_sales'],
                '地点': index['item_loc'],
                '商品详情页': index['detail_url'],
                '店铺链接': index['shopLink'],
                '图片链接': index['pic_url'],
            }
            # 将提取到的字典数据写入csv文件
            csvWriter.writerow(dict)
            print(dict, '\n')

print("爬取完成")
