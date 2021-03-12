# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 17:28:38 2020

@author: 范千惠
"""
import requests
#import traceback
from bs4 import BeautifulSoup

#返回url的源码
def getHTMLtext(url):
    try:
        kv={'user-agent':'Mozilla/5.0'}
        r=requests.get(url,timeout=30,headers=kv)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        #traceback.print_exc()
        print('error')
        return ""

#从东方财富网获得股票列表
def getStockLst(html,stocklst):
    soup=BeautifulSoup(html,'html.parser')
    tag_ul_lst=soup.find_all('div',id="quotesearch")[0]('ul')
    
    for i in range(len(tag_ul_lst)):
        tag_li_lst=[]
        tag_li_lst=tag_ul_lst[i].contents
        
        for j in range(len(tag_li_lst)):
            
            try:
                urlstg=tag_li_lst[j].contents[0].attrs['href']
                quote=urlstg.split('.html')[0][-8:].upper()
                stocklst.append(quote)
                #print("\r{}/{}".format(j,len(tag_li_lst)))
            except:
                continue

#从个股页面获得该股票的信息
def getStockinfo(html,dic):
    
    soup=BeautifulSoup(html,'html.parser')
    #储存名字
    stock_name=soup('div','stock-name')[0].string
    dic['stock-name']=stock_name
    #取出container标签
    container=soup('div','quote-container')[0]
    
    #取出stock-info标签
    stock_info=container('div','stock-info')[0]
    divlst=stock_info('div')
    dic['stock-info']={}
    for i in range(len(divlst)):
        if divlst[i].string:
            k=divlst[i].attrs['class'][0]
            v=divlst[i].string
            dic['stock-info'][k]=v
    
    #取出quote-info标签
    quote_info=container('table','quote-info')[0]
    tag_td_lst=quote_info('td')
    for i in range(len(tag_td_lst)):
        k=tag_td_lst[i].contents[0]
        v=tag_td_lst[i].contents[1].string
        dic[k]=v
        

def main():    
    #获得股票列表
    stocklst_url='http://quote.eastmoney.com/stock_list.html'
    html=getHTMLtext(stocklst_url)
    if not html:
        return
    stocklst=[]
    getStockLst(html,stocklst)
    #print(stocklst[0:10])
    
    #获得个股信息
    stockInfoLst=[]
    start_url='https://xueqiu.com/S/'
    for i in range(len(stocklst)):
        url=start_url+stocklst[i]
        single_html=getHTMLtext(url)
        #该股票页面存在
        if single_html:
            single_dic={}
            getStockinfo(single_html,single_dic)
            stockInfoLst.append(single_dic)
            print("\r {}/{}".format(i,len(stocklst)),end='')
    
    #设置数据储存文件的路径
    fpath='D:/stock_info.txt'
    with open(fpath,'a',encoding='utf-8') as f:
        for k in stockInfoLst:
            f.write(str(k)+'\n')

main()
    