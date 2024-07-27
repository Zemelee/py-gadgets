import requests
from lxml import etree

# 设置请求头
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
num = 43917687

url_list = []
title_list = []
# 获取1-5章节的链接
for i in range(num, num + 50):
    url = "https://www.ishuquge.com/txt/158004/{}.html".format(i)
    url_list.append(url)


# 获取每个章节对应源码
def parse_url(url):
    response = requests.get(url, headers=headers)
    return response.content.decode()


for url in url_list:
    # 用xpath解析链接内容
    tree = etree.HTML(parse_url(url))
    # 获取标题和章节
    title = tree.xpath('/html/body/div[4]/div[2]/h1/text()')
    print(title[0])
    title_list.append(title[0])
    # 获取正文
    # //*[@id="content"]
    content = tree.xpath('//*[@id="content"]/text()')
    with open("D:\PyGadgets\网络编程\practice\\article\{}.txt".format(title[0]),
              'w', encoding='utf-8') as file:
        for con in content:
            file.write(con)

print(title_list)
