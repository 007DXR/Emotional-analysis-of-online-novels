from networks import SentimentAnalysis, SentimentAnalysisBoson
import re
from matplotlib import pyplot as plt
from tqdm import tqdm, trange
import os
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool

SA = SentimentAnalysisBoson()


def cut_sent(para):
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")

def predict(sent):
    # print(sent)
    return SA.sentiment_score(sent)

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


def save_npz(filename):
    s, l = get_sentiment_score(filename)
    print(filename, np.mean(s), l)
    file_path='output_newdict_0405/'+filename.split('/')[-2]
    if os.path.exists(file_path)==False:
        os.makedirs(file_path)
    np.savez(file_path+'/'+filename.split('/')[-1][:-4], s)



# root_path = '/Users/zinccat/Documents/挑战杯/晋江2003~2021文包'
# os.chdir(root_path)
folders=['../网文分析/晋江2003~2021文包/2018-50本']
# save_npz('../网文分析/晋江2003~2021文包/2021-50本/《三嫁咸鱼》.txt')
for folder in folders:
    # outdir = '/Users/zinccat/Documents/挑战杯/outputs/2006'
    pool = ThreadPool(8)
    files=[]
    # files = [os.path.join(folder, filename) for filename in os.listdir(folder)]
    for filename in os.listdir(folder):
        files.append(folder+'/'+filename)
    pool.map(save_npz, files)
    pool.close()
    pool.join()

# save_npz(files)
# save_npz('/Users/zinccat/Documents/挑战杯/晋江2003~2021文包/2005-30本/又一春by大风刮过.txt')
# save_npz('/Users/zinccat/Documents/挑战杯/晋江2003~2021文包/2020-50本/难哄by竹已.txt')
# save_npz('/Users/zinccat/Documents/挑战杯/晋江2003~2021文包/2018-50本/《AWM[绝地求生]》作者：漫漫何其多.txt')