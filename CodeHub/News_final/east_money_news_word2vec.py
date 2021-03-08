# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 09:51:51 2020

@author: 范千惠
"""
### 用到的库
import jieba #分词
import jieba.analyse
from gensim.models import word2vec #训练词向量
import logging
import os
import re

### 去除非中文字符
with open('./data/east_money_news','r', encoding='utf-8') as f:
    with open('./data/east_money_news.txt','w', encoding='utf-8') as fw:
        # 读入原始新闻文本
        for line in f:
            result_line=''
            for uchar in line:
                if uchar >= u'u4e00' and uchar <= u'\u9fa5':
                    result_line += uchar
            fw.write(result_line+'\n')    
f.close()
fw.close()

### 新闻来源词频修改
# ./data/news_sources.config 文件从存放新闻来源，按需修改
# 目的：不分开固定词组
f_ns = open('./data/news_sources.config', 'r', encoding= 'utf-8')
sources = f_ns.read().split()
for source in sources:
    jieba.suggest_freq(source, True)

### 导入停用词表
#从文件导入停用词表
#把新闻来源也加入停用词表
stpwrdpath = "./data/stop_words.txt"
stpwrd_dic = open(stpwrdpath, 'r', encoding='utf-8')
stpwrd_content = stpwrd_dic.read()
#将停用词表转换为list  
stpwrdlst = stpwrd_content.splitlines()
stpwrd_dic.close()

### 分词
with open('./data/east_money_news.txt',encoding='utf-8') as f:
    # 读入原始新闻文本
    document = f.read()
    # 分词后去除列表中的停用词
    document_cut=[]
    document_cut += [word for word in jieba.cut(document) if word not in stpwrdlst]
    # 用空格分隔分词结果，形成分词后文本
    result = ' '.join(document_cut)
    
    with open('./data/east_money_news01.txt', 'w', encoding='utf-8') as f2:
        f2.write(result)
f.close()
f2.close()

### word2vec 模型训练
# 开启日志记录
# logging.basicConfig(format=
#                     '%(asctime)s : %(levelname)s : %(message)s'
#                     , level=logging.INFO)
# 使用 word2vec 提供的 LineSentence 类来读文件
sentences = word2vec.LineSentence(
    './data/east_money_news01.txt'
) 
# 建立模型 （ 暂时使用了默认参数 ）
model = word2vec.Word2Vec(
    sentences, hs=1,min_count=1,window=3,size=100
)

### 打印模型中词频最高的前 100 个词，写入./data/results/hotwords.result 文件
with open('./data/results/hotwords.result', 'w', encoding='utf-8') as f_rst:
    for i, word in enumerate(model.wv.vocab):
        if i == 100:
            break
        f_rst.write(word+'\n')

'''
#通过词向量，找出与目标词关系最近的前 20 个词
for key in model.wv.similar_by_word('黑龙江', topn =30):
        print(key[0], key[1])
'''
