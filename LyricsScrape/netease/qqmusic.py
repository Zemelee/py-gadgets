from gevent import monkey

monkey.patch_all()
# patch_all()能把程序变成协作式运行，帮助程序实现异步，需要放在最前面
# 利用协程和队列加快爬虫速度
# 上面两个语句必须放在最上面（不然会有Warning）
from gevent.queue import Queue
import gevent
import requests
from bs4 import BeautifulSoup
import html
import time
import pandas as pd
if __name__ == '__main__':
    def getMusicInfo():
        # 对url进行请求
        # 歌曲地址
        url = 'https://y.qq.com/n/yqq/singer/001Yxpxc0OaUUX.html#stat=y_new.song.header.singername'
        # UA伪装
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/89.0.4389.82 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers).text
        # 歌曲名、所属专辑、播放时长、播放链接、歌词、评论（日期、内容、点赞数量）
        # 使用Beautiful Soup进行 数据解析
        # 先实例化
        soup = BeautifulSoup(response, 'lxml')
        # 先找到大致范围
        temp = soup.find('li', mid=5408217)
        # 再根据要求缩小范围
        song_name = temp.select('div .songlist__songname span a')[0]
        song_album = temp.select('div .songlist__album a')[0]
        # 获取到了音乐播放链接、歌曲名、所属专辑连接、专辑名
        music_url = 'https:' + song_name['href']
        music_name = song_name['title']
        music_length = temp.select('div .songlist__time')[0].text
        album_url = 'https:' + song_album['href']
        album_name = song_album['title']

        # 再对详情页进行请求
        new_url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_yqq.fcg?nobase64=1&musicid=5408217&-=jsonp1&g_tk_new_20200303=1458790511&g_tk=1458790511&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0'
        # 这里要加上Referer（破解反爬）
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/89.0.4389.82 Safari/537.36',
            'Referer': 'https://y.qq.com/n/yqq/song/001NmPTG1fVsUw.html'
        }
        new_response = requests.get(url=new_url, headers=headers).json()
        music_lyric = new_response['lyric']

        # 将提取到的歌词内容进行html转义
        music_lyric = html.unescape(music_lyric)
        # 将歌词存入txt文件
        with open('music_lytic.txt', 'w', encoding='gbk') as fp:
            fp.write(music_lyric)
        musicDF = pd.DataFrame(columns=['歌曲名', '歌曲长度', '所属专辑名', '歌曲链接', '专辑链接'],
                               data=([[music_name, music_length, album_name, music_url, album_url]]))
        print(musicDF)
        # 转换成csv格式
        musicDF.to_csv('歌曲介绍.csv', encoding='gbk')


    # 提取评论（精彩和最新）
    # 精彩评论和最新评论区别在于参数不同！
    # UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.82 Safari/537.36'
    }


    def getAmazedComment():
        comment_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg'
        # 创建队列对象
        work = Queue()
        for i in range(0, 20):
            amazedParams = {
                'g_tk_new_20200303': '1458790511',
                'g_tk': '1458790511',
                'loginUin': '0',
                'hostUin': '0',
                'format': 'json',
                'inCharset': 'utf8',
                'outCharset': 'GB2312',
                'notice': '0',
                'platform': 'yqq.json',
                'needNewCode': '0',
                'cid': '205360772',
                'reqtype': '2',
                'biztype': '1',
                'topid': '5408217',
                'cmd': '6',
                'needmusiccrit': '0',
                'pagenum': i,  # 这里代表第几页（作为我们的参数）
                'pagesize': '20',  # 这里代表每页显示多少内容
                'lasthotcommentid': 'song_5408217_2512400045_1484758075',
                'domain': 'qq.com',
                'ct': '24',
                'cv': '10101010'
            }
            # 放入work队列中
            work.put_nowait(amazedParams)

        total_Dict = {'评论Id': [], '发布时间': [], '用户名': [], '评论内容': [], '点赞数': []}

        def getInfo():
            # 这里一共提取了 20*20=400条评论
            while not work.empty():
                # 精彩评论提取和存储
                params = work.get_nowait()
                amazedComment_response = requests.get(url=comment_url, params=params, headers=headers).json()
                amazedComment_list = amazedComment_response['comment']['commentlist']
                for i in amazedComment_list:
                    # 这里最好使用dict.get()方法，避免某项数据为空时报错
                    total_Dict['评论Id'].append(i.get('commentid', 'NULL'))
                    total_Dict['点赞数'].append(i.get('praisenum', 'NULL'))
                    if i.get('time', 'NULL') != 'NULL':
                        # 要将10位秒时间转成正常形式
                        tupTime = time.localtime(int(i.get('time')))
                        temp_time = time.strftime('%Y-%m-%d %H:%M:%S', tupTime)
                        total_Dict['发布时间'].append(temp_time)
                    else:
                        total_Dict['发布时间'].append('NULL')
                    total_Dict['用户名'].append(i.get('nick', 'NULL'))
                    total_Dict['评论内容'].append(i.get('rootcommentcontent', 'NULL'))

        # 创建空任务列表
        task_list = []
        # 这里代表使用多少个协程（开的越多速度越快，并且能够很好地支持高并发）
        # 速度还会受很多因素限制
        for i in range(3):
            # 使用gevent.spawn来让普通函数成为gevent任务
            task = gevent.spawn(getInfo())
            task_list.append(task)
        # 执行任务列表中的所有任务（开始爬取网站）
        gevent.joinall(task_list)

        print('获取热门评论完成！')
        total_Dict = pd.DataFrame(total_Dict)
        print(total_Dict)
        # 转换成csv格式
        total_Dict.to_csv('热门评论.csv', encoding='gbk')


    # 获取最新评论
    def getNewcomment():
        comment_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg'
        # 创建队列对象
        work = Queue()
        for i in range(0, 20):
            newParams = {
                'g_tk_new_20200303': '1458790511',
                'g_tk': '1458790511',
                'loginUin': '0',
                'hostUin': '0',
                'format': 'json',
                'inCharset': 'utf8',
                'outCharset': 'GB2312',
                'notice': '0',
                'platform': 'yqq.json',
                'needNewCode': '0',
                'cid': '205360772',
                'reqtype': '2',
                'biztype': '1',
                'topid': '5408217',
                'cmd': '8',
                'needmusiccrit': '0',
                'pagenum': i,
                'pagesize': '25',
                'lasthotcommentid': 'song_5408217_2631124132_1615512647',
                'domain': 'qq.com',
                'ct': '24',
                'cv': '10101010'
            }
            # 放入work队列中
            work.put_nowait(newParams)

        total_Dict = {'评论Id': [], '发布时间': [], '用户名': [], '评论内容': [], '点赞数': []}

        def getInfo():
            # 这里一共提取了 20*25=500条评论
            while not work.empty():
                # 精彩评论提取和存储
                params = work.get_nowait()
                amazedComment_response = requests.get(url=comment_url, params=params, headers=headers).json()
                amazedComment_list = amazedComment_response['comment']['commentlist']
                for i in amazedComment_list:
                    total_Dict['评论Id'].append(i.get('commentid', 'NULL'))
                    total_Dict['点赞数'].append(i.get('praisenum', 'NULL'))
                    if i.get('time', 'NULL') != 'NULL':
                        # 要将10位秒时间转成正常形式
                        tupTime = time.localtime(int(i.get('time')))
                        temp_time = time.strftime('%Y-%m-%d %H:%M:%S', tupTime)
                        total_Dict['发布时间'].append(temp_time)
                    else:
                        total_Dict['发布时间'].append('NULL')
                    total_Dict['用户名'].append(i.get('nick', 'NULL'))
                    total_Dict['评论内容'].append(i.get('rootcommentcontent', 'NULL'))

        # 创建空任务列表
        task_list = []
        # 这里代表使用多少个协程（开的越多速度越快，并且能够很好地支持高并发）
        # 速度还会受很多因素限制
        for i in range(3):
            # 使用gevent.spawn来让普通函数成为gevent任务
            task = gevent.spawn(getInfo())
            task_list.append(task)
        # 执行任务列表中的所有任务（开始爬取网站）
        gevent.joinall(task_list)

        print('获取最新评论完成！')
        total_Dict = pd.DataFrame(total_Dict)
        print(total_Dict)
        # 转换成csv格式
        # 这里不能用gbk编码，会报错，用utf_8_sig是比较保守的！（utf-8会中文乱码）
        total_Dict.to_csv('最新评论.csv', encoding='utf_8_sig')


    # 测试
    getMusicInfo()
    getAmazedComment()
    getNewcomment()

