from pandas import DataFrame
from py2neo import Graph,Node,Relationship,NodeMatcher
import pandas as pd
import numpy as np
import os

# 连接Neo4j数据库
graph = Graph('http://localhost:7474/db/data/',username='neo4j',password='fqh123123')

# 删除所有节点
graph.run('MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r')

# 读取数据
stock = pd.read_csv('test\\stock_basic.csv',encoding="gbk")
executive = pd.read_csv('test\\executive.csv',encoding='gbk')

# 处理数据
stock['行业'] = stock['行业'].fillna('未知')  # 去除NAN
executive=executive.fillna('未知')
chairman = pd.DataFrame(executive['法人代表']) # 获取法人数据，其他数据暂时没加入
chairman.drop_duplicates(subset=None, keep='first',inplace=True) # 去重一下，先假设所有同名则人物相同


matcher = NodeMatcher(graph)

# 创建结点：行业
# 处理数据
industry = pd.DataFrame(stock['行业'])
industry.drop_duplicates(subset=None, keep='first',inplace=True)
for i in industry.values:
    a = Node("行业",名称=i[0],测试='None')
    graph.create(a)


# 创建结点：股票
# 创建关系：股票-行业
for i in stock.values:
    a = Node("股票",名称=i[3],代码=str(i[2]).zfill(6))
    graph.create(a)

    b = matcher.match("行业",名称=i[4]).first()
    r = Relationship(a, "所属行业", b)
    graph.create(r)

# 创建结点：法人
for i in chairman.values:
    a = Node("人",姓名=i[0])
    graph.create(a)


# 创建关系：法人-股票
for i in executive.values:
    a = matcher.match("股票", 代码=i[1].split('.')[0]).first()
    b= matcher.match("人",姓名=i[2]).first()
    if (a == None or b == None):
        continue

    r = Relationship(a,"法人代表",b)
    graph.create(r)
