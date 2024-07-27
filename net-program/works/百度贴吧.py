import requests
import re

# 设置请求头，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# 热门帖子的 URL

url = 'https://tieba.baidu.com/p/8276364061'

storey = 1

for pn in range(5):
    url = 'https://tieba.baidu.com/p/8276364061?pn={}'.format(pn)
    # 发送 GET 请求，获取页面内容
    response = requests.get(url, headers=headers)
    content = response.content.decode()
    # print(content)

    # 提取发帖人
    author_pattern = r'class="p_author_name j_user_card" href="(.*?)">(.*?)</a>'
    author = re.search(author_pattern, content).group(2)

    # 提取发帖时间
    time_pattern = r':&quot;202(.*?)&quot;,&quot;'
    time = '202' + re.search(time_pattern, content).group(1)

    # 提取楼层数和回帖内容
    post_pattern = r'<div id="post_content_\d+" class="d_post_content j_d_post_content  clearfix" style="display:;">(.*?)<'
    post_matches = re.findall(post_pattern, content)
    # print(post_matches)
    floor = len(post_matches)
    # 提取点赞数
    like_pattern = r'<span class="red">(.*?)</span>'
    like_matches = re.findall(like_pattern, content)
    likes = [int(match) for match in like_matches if match.isdigit()]

    # 输出结果
    print('发帖人：', author)
    print('发帖时间：', time)
    print("页数：", pn + 1)
    print('楼层数：', floor)
    for i in range(floor):
        print('第', i + 1, '层回帖：', post_matches[i])
