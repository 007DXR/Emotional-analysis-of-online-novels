# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 10:28:41 2020

@author: cm
"""

from networks import SentimentAnalysis
import re
from matplotlib import pyplot as plt
from tqdm import tqdm, trange


SA = SentimentAnalysis()


def predict(sent):
    """
    1: positif
    0: neutral
    -1: negatif
    """
    score1,score0 = SA.normalization_score(sent)
    if score1 == score0:
        result = 0
    elif score1 > score0:
        result = 1
    elif score1 < score0:
        result = -1
    return score1 - score0 #result

# 版本为python3，如果为python2需要在字符串前面加上u


def cut_sent(para):
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")
        

if __name__ =='__main__':
    # text = '对你不满意'
    # text = '大美女'
    # text = '帅哥'
    # text = '我妈说明儿不让出去玩'
    s = []
    for i in range(1, 133):
        with open("/Users/zinccat/Documents/挑战杯/废后将军文本/第{}章.txt".format(i), 'r', encoding='utf-8') as f:
            text = f.read()
            text = cut_sent(text)
            text = list(filter(None, text))
        for w in text:
            s.append(predict(w))
    n_list = [2, 10, 100, 500, 1000]
    for n in n_list:
        l = []
        sc = 0
        for i in trange(1, len(s)):
            sc += s[i-1]
            if i >= n:
                sc -= s[i-n]
                l.append(sc/(n-1))
            # else:
            #     l.append(sc/i)
        # idxes = list(range(1, len(outputs)))
        plt.plot(l)
        plt.xlabel("Sentence")
        plt.ylabel("Sentiment Score")
        plt.title("Sentiment Score of Each Sentence (Revive {})".format(n-1))
        plt.savefig("/Users/zinccat/Documents/挑战杯/废后将军文本/图{}.png".format(n-1))

