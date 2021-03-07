import tushare as ts
import pandas as pd

# 新版tushare需要个人token
ts.set_token('84cc8b9e382b572f6094b5b9963eeb92ff449bd4a7c4590bde2b9c00')
pro = ts.pro_api()

# 1. 获取股票基本信息:Tscode 代码 名称 行业 市场类型
# -------------------------------------------------------------------------------------
stock_basic = pro.stock_basic(list_status='L', fields='ts_code, symbol, name, industry,market')
# 重命名行，便于后面导入neo4j
basic_rename = {'ts_code': 'TS代码', 'symbol': '股票代码', 'name': '股票名称', 'industry': '行业','market':'市场类型'}
stock_basic.rename(columns=basic_rename, inplace=True)

# 保存为stock_basic.csv
stock_basic.to_csv('info\\stock_basic.csv', encoding='gbk')
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# 2. 获取上市公司法人信息及城市信息
executive = pro.stock_company(exchange='', fields='ts_code,chairman,manager,secretary,city')
executive_rename = {'ts_code':'TS代码','chairman':'法人代表','manager':'总经理','secretary':'董秘','city':'城市'}
executive.rename(columns = executive_rename,inplace=True)
executive.dropna()

# 保存为executive.csv
executive.to_csv('info\\executive.csv', encoding='gbk')
# -------------------------------------------------------------------------------------

# # -------------------------------------------------------------------------------------
# # 3. 获取上市公司股东信息
# holder_all = pd.DataFrame(columns=["TS代码","股东名称","持股比例"])
#
# # 每个股票选择五个持股比例最高的股东数据
# for row in range(len(stock_basic)):
#     TS_code = stock_basic.iloc[row]['TS代码'] # 获取股票代码
#     holder = pro.top10_holders(ts_code=TS_code,exchange='', fields='ts_code,holder_name,hold_ratio') # 获取该股票的股东
#     # 取出五个持股比例最高
#     holder.sort_values(by='hold_ratio',ascending=False,inplace=True)
#     holder.drop_duplicates(subset='holder_name',inplace=True)
#     holder=holder[:5]
#     holder_rename = {'ts_code':'TS代码','holder_name':'股东名称','hold_ratio':'持股比例'}
#     holder.rename(columns = holder_rename,inplace=True)
#     # 拼接
#     holder_all = pd.concat([holder_all,holder])
#
# # 保存为holder.csv
# holder_all.to_csv('info\\holder.csv', encoding='gbk')
# # -------------------------------------------------------------------------------------
