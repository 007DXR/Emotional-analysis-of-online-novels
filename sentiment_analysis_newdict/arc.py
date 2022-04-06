# -*- coding: utf-8 -*-

# 导入一些库, 没有的话需要安装
# 即在命令行运行下一句
# pip install matplotlib tqdm numpy

from networks import SentimentAnalysis
import re
from matplotlib import pyplot as plt
from tqdm import tqdm, trange
import numpy as np


SA = SentimentAnalysis()

# 评分函数


def predict(sent):
    """
    1: positif
    0: neutral
    -1: negatif
    """
    score1, score0 = SA.normalization_score(sent)
    if score1 == score0:
        result = 0
    elif score1 > score0:
        result = 1
    elif score1 < score0:
        result = -1
    return score1 - score0  # result

# 版本为python3，如果为python2需要在字符串前面加上u


# 分句函数
def cut_sent(para):
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")


s = []
# 把此处的文件位置改成要分析的文件位置
with open("/Users/zinccat/Documents/挑战杯/晋江2003~2021文包/2004-30本/《爱云风情》作者：暗香飞花.txt", 'r', encoding='utf-8') as f:
    text = f.read()
    text = cut_sent(text)
    text = list(filter(None, text))
for w in text:
    s.append(predict(w))

# 绘制弧线
# n_list = [2, 10, 100, 500, 1000, 2000]
# for n in n_list:
#     l = []
#     sc = 0
#     for i in trange(1, len(s)):
#         sc += s[i-1]
#         if i >= n:
#             sc -= s[i-n]
#             l.append(sc/(n-1))
#     plt.figure(figsize=(40, 20))
#     plt.plot(l)
#     plt.ylabel("Sentiment Score")
#     plt.title("Sentiment Score of Each Sentence ({})".format(n-1))
#     plt.show()

l = []
points = 100
n = 80
step = (len(s)-n) // points
idx = [step*i for i in range(points)]
sc = 0
for i in trange(1, len(s)):
    sc += s[i-1]
    if i >= n:
        sc -= s[i-n]
        l.append(sc/(n-1))
l = np.array(l)
l = l[idx]
print(len(l))
plt.figure(figsize=(40, 20))
plt.plot(l)
plt.ylabel("Sentiment Score")
plt.title("Sentiment Score of Each Sentence ({})".format(n-1))
plt.show()
