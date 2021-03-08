# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 09:51:51 2020

@author: 范千惠
"""

import requests 
import re
import traceback
from bs4 import BeautifulSoup

def getHTMLtext(url):
    #print("start getHTMLtext")
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        print('error')
        return ""


def getUrlLst(ulst,html):
    #print("start getUrlLst")
    soup=BeautifulSoup(html,'html.parser')
    a=soup.find_all('div','item')
    for i in range(len(a)):
        target=a[i].contents[1]
        #print(a[i].contents)
        ulst.append(target.attrs['href'])


def getSerielPageHTML(url,htmlst):
    n=2;
    html=getHTMLtext(url)
    while html:
        htmlst.append(html)
        if(n>25):
            break
        url_n=url.split('.html')[0]+'_'+str(n)+'.html'
        print(url_n)
        html=getHTMLtext(url_n)
        n+=1

    print(len(htmlst))


def dealSinglePage(html):
    
    nlst=[]
    flag=getNewsTre(nlst,html)
    #该页面存在新闻则写入文档
    if flag:
        fpath='./data/east_money_news'
        with open(fpath,'a',encoding='utf-8') as f:
            for dicnews in nlst:
                f.write(str(dicnews)+'\n')
    #不存在则跳过


def getNewsTre(nlst,html):
    soup=BeautifulSoup(html,'html.parser')
    taglist=soup.find_all('li',id=re.compile(r'^newsTr'))
    #该页面未找到新闻树
    if len(taglist)==0:
        return 0
    #该页面找到新闻树
    for i in range(len(taglist)):
        tagp=taglist[i]('p')
        #print(tagp)
        dic={}
        for j in range(len(tagp)):
            attrs=tagp[j].attrs
#            if(attrs['class']==['title']):
#                if len(tagp[j]('a'))==1:
#                    dic['title']=tagp[j]('a')[0].string
#                    if tagp[j]('a')[0].attrs['href']:
#                        dic['url']=tagp[j]('a')[0].attrs['href']
            if(attrs['class']==['info']):
                try:
                    dic['info']=tagp[j].attrs['title']
                except:
                    dic['info']=tagp[j].string  
            elif(attrs['class']==['time']):
                dic['time']=tagp[j].string
        #单条新闻字典压入列表
        nlst.append(dic)
    return 1

    
def getNewsDtl(ndic,nlst):
    pass


def main():
    #print("start main")
    start_url="http://finance.eastmoney.com/a/cjjsp.html"
    start_html=getHTMLtext(start_url)

    if not start_html:
        print("start getHTMLtext error")
        return ''
    ulst=[]
    getUrlLst(ulst,start_html)

    #逐模块链接搜索
    for i in range(len(ulst)):
        print("当前进度：{}/{}".format(i,len(ulst)))
        try:
            htmlst=[]
            getSerielPageHTML(ulst[i],htmlst)
            for j in range(len(htmlst)):    
                dealSinglePage(htmlst[j])
        except:
            traceback.print_exc()
            print('ulst error')
            continue

print("start")
main()

