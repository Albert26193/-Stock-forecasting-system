import tushare as ts
import pandas as pd

ts.set_token('87109caa5d7d9197ce7c5d2cd687bf6d8f1fef7f98042675c147012b')  # 新版tushare需要个人token
pro = ts.pro_api()

# <class 'pandas.core.frame.DataFrame'>

# 获取股票基本信息:TS代码 股票代码 股票名称 行业..
# 概念无权限获取
# %%
stock_basic = pro.stock_basic(list_status='L', fields='ts_code, symbol, name, industry,market')
# 重命名行，便于后面导入neo4j
basic_rename = {'ts_code': 'TS代码', 'symbol': '股票代码', 'name': '股票名称', 'industry': '行业','market':'市场类型'}
stock_basic.rename(columns=basic_rename, inplace=True)

# 保存为stock_basic.csv
stock_basic.to_csv('test\\stock_basic.csv', encoding='gbk')
stock_basic.head()
# %%

# 获取上市公司法人信息及城市信息：年龄信息等tushare暂时权限不够
# %%n
executive = pro.stock_company(exchange='', fields='ts_code,chairman,manager,secretary,city')
executive_rename = {'ts_code':'TS代码','chairman':'法人代表','manager':'总经理','secretary':'董秘','city':'城市'}
executive.rename(columns = executive_rename,inplace=True)

# 保存为executive.csv
executive.to_csv('test\\executive.csv', encoding='gbk')
executive.head()
# %%

# for i in executive.values:
#     print(i[0])