# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 14:47:22 2020

@author: 94859
"""

#Requests库的通用代码框架
import requests
import os
#
#def getHTTP(url):
#    try:
#        r=requests.get(url,timeout=300)
#        r.raise_for_status()   #抛出异常
#        r.encoding=r.apparent_encoding
#    except:
#        print("出现异常")
#    return r
#
#r=getHTTP("https://item.jd.com/26178305228.html")
#print(r)

path="D:\\fqh_Workspace\\Quantitative_investment\\test.jpg"
url="http://image.nationalgeographic.com.cn/2017/1121/20171121023827320.jpg"

try:
    if not os.path.exists(path):
        r=requests.get(url)
        r.raise_for_status()
        with open(path,'wb') as f:
            f.write(r.content)
            f.close()
            print("文件保存成功")
    else:
        print("文件已存在")
except:
    print("爬取失败")