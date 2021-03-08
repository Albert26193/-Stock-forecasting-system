# NEWS_FINAL 新闻模块

## 文件结构
```
`-------- east_money_news_spider.py 
            新闻爬虫，新闻写入 data/east_money_news
    |
    `---- east_money_news_word2vec.py 
            新闻分词及词向量训练 + 词频分析，top100热词写入 data/results/hotwords.result
    |
    `---- data 各类数据文件
            |
            `---- east_money_news 新闻文本原始文件（结构文件）
            |
            `---- east_money_news.txt 新闻文本纯中文文件
            |
            `---- east_money_news01.txt 新闻分词文件
            |
            `---- stop_words.txt 停用词表
            |
            `---- news_sources.config 新闻来源词汇
            |
            `---- results
                |
                `---- hotwords.result top100热词结果文件

```

## python 依赖库
#### east_money_news_spider.py
```
 requests
 re
 traceback
 bs4
```
#### east_money_news_word2vec.py
```
 numpy
 gensim
 jieba
 os
 logging
```
## 业务说明

"./data/east_money_news" 用于给前端提供新闻文本数据  
"./data/results/hotwords.result" 用于给前端提供热词数据




