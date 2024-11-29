import requests
from bs4 import BeautifulSoup
import re


# 清除艾特 //@username:
def clean_at(text):
    # Regular expression to match the system at texts
    pattern = r"//@[\u4e00-\u9fa5a-zA-Z0-9_-]+[: ]?+[ :]?"
    # Use re.sub to replace matched patterns with an empty string
    cleaned_text = re.sub(pattern, " ", text).strip()
    return cleaned_text

url = "https://s.weibo.com/weibo?q=%E7%94%9F%E8%82%B2%E7%8E%87&timescope=custom%3A2023-11-10%3A2024-11-09&page={}"


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "cookie": "ALF=1735305431; SUB=_2A25KQ2uHDeRhGeRN4lUW8SbLwzmIHXVpIeFPrDV8PUJbkNANLW7_kW1NU2cBwDpRok6WdYBbi4kGUpy5W4Px95nj; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhKqA.Ybu1M54C-OuVlCpWb5JpX5KzhUgL.Foz01KMNeKnN1h-2dJLoI0YLxK-LBKqLB--LxK-LB-BL1K5LxKqL1KnLB-qLxKBLBonLB-2LxKqLBKzLBKqLxKqL1heLBoeLxK-LB--LBoqt; SINAGLOBAL=4149350232805.2954.1732713434244; _s_tentry=-; Apache=9523180686954.098.1732877739971; ULV=1732877740035:2:2:2:9523180686954.098.1732877739971:1732713434310",
    "Referer": "https://s.weibo.com/weibo?q=%E7%94%9F%E8%82%B2%E7%8E%87&timescope=custom%3A2023-11-10%3A2024-11-09",
    "Referrer-Policy": "strict-origin-when-cross-origin",
}


# w写入模式(自动创建) a追加模式 x创建并写入(已存在会报错)
with open("weibo2.txt", "a", encoding="utf-8") as file:
    for page in range(1, 5):
        print(f"正在爬取第{page}页....")
        response = requests.get(url.format(page), headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        weibos = soup.find_all("div", class_="card-wrap")
        for weibo in weibos:
            content = weibo.find_all("p", attrs={"node-type": "feed_list_content"})
            full_content = weibo.find_all(
                "p", attrs={"node-type": "feed_list_content_full"}
            )
            if full_content:
                for fc in full_content:
                    file.write(clean_at(fc.text))
            else:
                for c in content:
                    file.write(clean_at(c.text)+"\n")
    file.write("\n")
