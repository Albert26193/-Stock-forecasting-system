# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 19:40:25 2020

@author: 94859
"""

import requests
from bs4 import BeautifulSoup
import traceback
import re

def getHTMLText(url):
    try:
        kv={'user-agent':'Mozilla/5.0'}
        r = requests.get(url, timeout = 30, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getStockList(lst, stockURL):
    html = getHTMLText(stockURL)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']    
            lst.append(re.findall(r"[s][h,z][\d]{6}",href)[0])
        except:
            continue

def getStockInfo(lst, stockURL, fpath):
    n=0
    for stock in lst:
        url = stockURL+'/S/'+stock.upper()
        
        html = getHTMLText(url)
        
        try:
            if html =="":
                continue
            infoDict = {}
            soup = BeautifulSoup(html,'html.parser')
            stockInfo = soup.find('div',attrs={'class':'container-sm float-left stock__main'})

            name = stockInfo.find_all(attrs={'class':'stock-name'})[0]

            infoDict.update({'股票名称':name.text.split()[0]})


            keyList = stockInfo.find_all('td')
            valueList = stockInfo.find_all('span')
            for i in range(len(keyList)):
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val

            with open(fpath, 'a', encoding='utf-8') as f:
                n+=1
                f.write(str(infoDict)+'\n')
                print('\r 当前进度{}/{}:'.format(n,len(lst)),end='')
        except:
            traceback.print_exc()
            continue
        
def main():
    stock_list_url = 'http://quote.eastmoney.com/stock_list.html'
    stock_info_url = 'https://xueqiu.com'
    output_file = 'D://股市.txt'
    slist =[]
    getStockList(slist, stock_list_url)
    getStockInfo(slist,stock_info_url,output_file)

main()