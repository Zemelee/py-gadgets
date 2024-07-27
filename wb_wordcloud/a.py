import requests
from bs4 import BeautifulSoup

# 地摊经济的URL

header = {
    'Host': 's.weibo.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.2.2007794384.1673230894; _gid=GA1.2.1601332821.1673230894; SINAGLOBAL=794726035907.9933.1673230907015; SUB=_2A25Ovw2FDeRhGeNG7VEV9CrPzzyIHXVqQ5PNrDV8PUJbkNANLUfjkW1NSyLJ9lFJZymsgL6QmsMBV3ZgNIf-Hhl5; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWT0TTFicp.YcVXQIdAY_y-5NHD95Qf1hq0ShBXe0B7Ws4Dqcj_i--fi-isi-8Fi--Xi-zRiKyFi--4iKLFi-2Ri--Xi-iWiKnci--fiK.7iK.N; wvr=6; PC_TOKEN=c3976ce391; _s_tentry=www.baidu.com; UOR=www.baidu.com,weibo.com,www.baidu.com; Apache=3305112191000.201.1673253240421; ULV=1673253240452:2:2:2:3305112191000.201.1673253240421:1673230907019; webim_unReadCount=%7B%22time%22%3A1673253247152%2C%22dm_pub_total%22%3A28%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A30%2C%22msgbox%22%3A0%7D',
}
print("开始爬取2021年微博....")
for page in range(0, 41):
    print("正在爬取第{}页...".format(page + 1))
    url = f'https://s.weibo.com/weibo?q=%E5%9C%B0%E6%91%8A%E7%BB%8F%E6%B5%8E&timescope=custom:2022-01-02:2023-01-09&page={page}'
    # 发送HTTP GET请求并获取响应
    response = requests.get(url, headers=header)
    # 使用Beautiful Soup解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')
    # 在HTML中查找所有class为'txt'的p元素
    weibo_ps = soup.find_all('p', class_='txt')

    # 遍历每个p元素，提取微博内容
    with open("2022.txt", 'a', encoding='utf-8') as f:
        for p in weibo_ps:
            # 使用get_text()方法获取div中的文本
            weibo_text = p.get_text()
            f.write(weibo_text)
            print("写入内容：", weibo_text)
