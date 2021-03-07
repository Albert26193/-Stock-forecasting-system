from pandas import DataFrame
from py2neo import Graph,Node,Relationship,NodeMatcher
import pandas as pd
import numpy as np
import os

# 连接Neo4j数据库
graph = Graph('http://localhost:7474/db/data/',username='neo4j',password='root123')
# 图数据库实例
matcher = NodeMatcher(graph)

# 初始化 ： 删除所有节点
graph.run('MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r')

# 读取数据
Stock = pd.read_csv('info\\stock_basic.csv',encoding="gbk")
Stock = Stock.dropna()
Executive = pd.read_csv('info\\executive.csv',encoding='gbk')
Executive = Executive.dropna()
Holder = pd.read_csv('info\\holder.csv',encoding='gbk')
Holder = Holder.dropna()

# 创建结点：行业
Stock['行业'] = Stock['行业'].fillna('未知') # 处理数据
industry = pd.DataFrame(Stock['行业'])
industry.drop_duplicates(subset=None, keep='first',inplace=True) # 去重
for i in industry.values:
    a = Node("行业",名称=i[0])
    graph.create(a)


# 创建结点：城市
city = pd.DataFrame(Executive['城市']).fillna('未知')
city.drop_duplicates(subset=None, keep='first',inplace=True) # 去重
for i in city.values:
    a = Node("城市",名称=i[0])
    graph.create(a)


# 创建结点：法人
chairman = pd.DataFrame(Executive['法人代表']).fillna('未知')
chairman.drop_duplicates(subset=None, keep='first',inplace=True) # 去重
for i in chairman.values:
    a = Node("法人",姓名=i[0])
    graph.create(a)

# 创建结点：股东
holders = pd.DataFrame(Holder['股东名称']).fillna('未知')
holders.drop_duplicates(subset=None, keep='first',inplace=True) # 去重
for i in holders.values:
    a = Node("股东",名称=i[0])
    graph.create(a)

# 创建结点：股票
# 创建关系：股票-(所属行业)-行业
for i in Stock.values:
    a = Node("股票",名称=i[3],代码=str(i[1]).replace('.',''))
    graph.create(a)

    b = matcher.match("行业",名称=i[4]).first()
    r = Relationship(a, "所属行业", b)
    graph.create(r)

# 创建关系：股票-(法人代表)-法人
# 创建关系：股票-(所在城市)-城市
for i in Executive.values:
    a = matcher.match("股票", 代码=i[1].replace('.','')).first()
    b= matcher.match("法人",姓名=i[2]).first()
    c = matcher.match("城市", 名称=i[5]).first()

    if (a != None and b != None):
        r = Relationship(a,"法人代表",b)
        graph.create(r)

    if (a != None and c != None):
        r = Relationship(a, "所在城市", c)
        graph.create(r)


# 关键关系：股东-(持股)-股票
for i in Holder.values:
    a = matcher.match("股东",名称=i[2]).first()
    b = matcher.match("股票", 代码=i[1].replace('.','')).first()

    if (a != None and b != None):
        properties = {'持股比例': i[3]}
        r = Relationship(a,"持股",b,**properties)
        graph.create(r)
