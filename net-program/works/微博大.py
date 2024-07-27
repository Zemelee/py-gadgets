# 导入相关库
import requests
import json
import re

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}
# 设置要爬取的大V的微博ID
weibo_id = '1265020392'
# 设置要爬取的页数
page_num = 1
# 构造请求url
url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' \
      + weibo_id + '&containerid=107603' + weibo_id
# 循环爬取每一页的数据
for page in range(1, page_num + 1):
    params = {
        'page': page
    }
    response = requests.get(url, headers=headers, params=params)
    json_data = json.loads(response.text)
    trip = json_data['data']['cards']
    for i in trip:
        # 获取点赞数
        zan = i['mblog']['attitudes_count']
        # 获取微博内容
        weibo_content = i['mblog']['text']  # (<[^>\s]+)\s[^>]+?(>)
        weibo_content = re.sub(r'<.*?>', r'', weibo_content)
        # 获取评论数
        remarks_num = i['mblog']['comments_count']
        print("正文内容:", weibo_content)
        print('点赞数：', zan)
        print('评论数：', remarks_num)
        # 获取评论内容
        comments = i['mblog']  # region_name
        print(comments['region_name'])
        print('-' * 100)
