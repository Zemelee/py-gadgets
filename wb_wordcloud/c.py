import jieba

txt = open("2020.txt", "r", encoding="utf-8").read()
words = jieba.lcut(txt)
# print(words)
wordsDict = {}  # 新建字典用于储存词及词频
for word in words:
    if len(word) == 1:  # 单个的字符不作为词放入字典(其中包括标点)
        continue
    elif word.isdigit() == True:  # 剔除数字
        continue
    elif word in wordsDict:
        wordsDict[word] += 1  # 对于重复出现的词，每出现一次，次数增加1
    else:
        wordsDict[word] = 1

wordsDict_seq = sorted(wordsDict.items(), key=lambda x: x[1], reverse=True)  # 按字典的值降序排序
# wordsDict_seq #此行代码便于从全部中选取不需要的关键词
print(wordsDict_seq[:15])  # 查看前15个
