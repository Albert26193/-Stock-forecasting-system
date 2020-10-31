import tushare as ts
import hashlib
import pandas

ts.set_token('87109caa5d7d9197ce7c5d2cd687bf6d8f1fef7f98042675c147012b') # 新版tushare需要个人token
pro = ts.pro_api()


# <class 'pandas.core.frame.DataFrame'>
data1 = pro.stock_company(exchange='', fields='ts_code,chairman,manager,secretary,city')
data1.to_csv("data1.csv",encoding="utf-8")
print(data1)


data2 = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name,industry,market')
data2.to_csv("data2.csv",encoding="utf-8")
print(data2)
#

# datas = pro.query('stock_basic', exchange='', list_status='L', fields='symbol,name,area,industry')
#
#
# df = pro.stock_company(exchange='SZSE', fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province')
# df.sort_values(by=['ts_code'])
#
# lists = datas[0:10]
#
# print(datas)
# print(datas.iloc[1,3])
# # print(df)
#
# # md5加密成唯一id
# def get_md5(string):
#     """Get md5 according to the string
#     """
#     byte_string = string.encode("utf-8")
#     md5 = hashlib.md5()
#     md5.update(byte_string)
#     result = md5.hexdigest()
#     return result
#
# print(get_md5("qjy"))
# print(get_md5("q"))
# print(get_md5("qjy"))