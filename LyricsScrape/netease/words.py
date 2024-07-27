import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image

final = ""
filename = r"2.txt"

with open(filename, 'r', encoding='utf-8') as f:
    # txt = f.read()
    for line in f.readlines():
        temp = jieba.lcut(line)
        for i in temp:
            if len(i) >= 2:
                final = final + i + ' '

    # res1 =  jieba.lcut(txt)
mask = np.array(Image.open("2.png"))
font = r'C:\Windows\fonts\msyh.ttc'
word_pic = WordCloud(
    collocations=False,
    font_path=font,
    height=1800,
    background_color=None,
    # mask=mask,
    random_state=50,  # 设置有多少种随机生成状态，即有多少种配色方案
    width=1800,
    margin=2) \
    .generate(final)

plt.imshow(word_pic)
plt.axis("off")
plt.show()
word_pic.to_file('1.png')

