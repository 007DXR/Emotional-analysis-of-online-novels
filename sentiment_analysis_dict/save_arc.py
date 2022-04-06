# -*- coding: utf-8 -*-

# 导入一些库, 没有的话需要安装
# 即把下一句注释掉再运行
# !pip install matplotlib tqdm numpy

from networks import SentimentAnalysis
import re
from matplotlib import pyplot as plt
from tqdm import tqdm, trange
import numpy as np
import os


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
    return score1 - score0 #result

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

def get_sentiment_score(filename):
    """
    获取全文情感分数
    """
    s = []
    # 把此处的文件位置改成要分析的文件位置
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
        text = cut_sent(text)
        text = list(filter(None, text))
    for w in text:
        s.append(predict(w))
    return s, len(s)

def savearc(filename, outdir='/Users/zinccat/Documents/挑战杯/arc_newdict', nmax=2000, points=200):
    try:
        s, length = get_sentiment_score(filename)
        # n = min(length//8, nmax+1)
        n = 15 * length//points
        step = (length - n)//points
        idx = [step*i for i in range(points)]
        l = []
        sc = 0
        for i in range(1, len(s)):
            sc += s[i-1]
            if i >= n:
                sc -= s[i-n]
                l.append(sc/(n-1))
        l = np.array(l)
        l = l[idx]
        os.makedirs(os.path.join(outdir, filename.split('/')[-2]), exist_ok=True)
        np.save(os.path.join(outdir, filename.split('/')[-2], filename.split('/')[-1][:-4]), l)
    except Exception as e:
        print(e)
        print(filename)

import os
from multiprocessing.dummy import Pool as ThreadPool

root_path = '/Users/zinccat/Documents/挑战杯/晋江2003~2021文包'
os.chdir(root_path)
for folder in tqdm(os.listdir(root_path)[3:5]):
    # outdir = '/Users/zinccat/Documents/挑战杯/outputs/2006'
    pool = ThreadPool(10)
    files = [os.path.join(root_path, folder, filename) for filename in os.listdir(folder)]
    pool.map(savearc, files)
    pool.close()
    pool.join()



