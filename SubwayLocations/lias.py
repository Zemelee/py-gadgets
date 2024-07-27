import random
import json
import requests

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Opera/8.0 (Windows NT 5.1; U; en)',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
]


# 解析json数据：
def getHtml(url):
    user_agent = random.choice(USER_AGENTS)
    headers = {
        "Host": "map.amap.com",
        'User-Agent': user_agent
    }
    try:
        response = requests.get(url, headers=headers)
        # print(response.url)
        text = response.content
        return text
    except:
        print("爬取失败!")


# 解析json数据：
def parse_page(text):
    lines_list = json.loads(text).get('l')
    # 地铁线路信息表
    lineInfo_list = []
    for line in lines_list:
        # 每条线的信息集合
        lineInfo = {}
        lineInfo['ln'] = line.get('ln')
        # print(lineInfo['ln'])
        # 线路站点列表
        station_list = []
        st_list = line.get('st')
        for st in st_list:
            station_dict = {}
            station_dict['name'] = st.get('n')
            coord = st.get('sl')
            station_dict['lat'] = coord.split(',')[0]
            station_dict['lon'] = coord.split(',')[-1]
            # print("站名称:", station_dict['name'])
            # print("经度：", station_dict['lat'])
            # print("纬度：", station_dict['lon'])
            station_list.append(station_dict)
            # pass
        # print('-----------------------------------')
        lineInfo['st'] = station_list
        lineInfo['kn'] = line.get('kn')
        lineInfo['ls'] = line.get('ls')
        lineInfo['cl'] = line.get('cl')
        lineInfo_list.append(lineInfo)
        print(lineInfo_list)
    # 返回各线路信息列表
    return lineInfo_list


# 保存站点数据（站名称、经纬度）：
def save_file(filename, lineInfo):
    print("开始写入文件......")
    with open(filename, 'a', encoding='utf-8') as f:
        for i in lineInfo:
            for st in i['st']:
                print(st)
                f.write(st['name'] + "  " + st['lat'] + "  " + st['lon'] + "\n")
    print("写入文件完成！")


url = 'http://map.amap.com/service/subway?_1661413505141&srhdata=5101_drw_chengdu.json'
text = getHtml(url)
lineInfo = parse_page(text)
# print(len(lineInfo))
filename = 'lias.txt'
save_file(filename, lineInfo)
