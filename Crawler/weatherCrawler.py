#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
# Author:taoke
import http.cookiejar
import re
import bs4
import urllib.request
import cityDic
import threading
import json

class ipAddrAreaCrawler(object):
    url = 'http://2018.ip138.com/ic.asp'
    ipAddrArea = None
    def __init__(self):
        self.ip = ''       #IP
        self.province = '' #省
        self.city = ''     #城市
        self.operator = '' #运营商
        self.start()

    def start(self):
        threading.Thread(target=self.startCrawler).start()

    def startCrawler(self):
        try:
            bytesdata = urllib.request.urlopen(ipAddrAreaCrawler.url).read()
            data = str(bytesdata, encoding='gb2312')
            pattern = re.compile('((1[0-9][0-9]\.)|(2[0-4][0-9]\.)|(25[0-5]\.)|([1-9][0-9]\.)|([0-9]\.)){3}((1[0-9][0-9])|(2[0-4][0-9])|(25[0-5])|([1-9][0-9])|([0-9]))')
            self.ip = pattern.search(data).group()
            pattern = re.compile('来自：.+?</ce')
            addr = pattern.search(data).group()[3:-4].split(' ')
            province_city = addr[0].split('省')
            self.province = province_city[0]
            self.city = province_city[1].split('市')[0]
            self.operator = addr[1]
            ipAddrAreaCrawler.ipAddrArea = (self.ip, self.province, self.city, self.operator)
        except:
            print('ipAddrAreaCrawler.startCrawler()  error')
            ipAddrAreaCrawler.ipAddrArea = None
    def getipAddArea(self):
        return ipAddrAreaCrawler.ipAddrArea

class weatherCrawler(object):
    mainUrl = 'http://www.nmc.cn'
    apiUrl =  'http://www.nmc.cn/f/rest/aqi/'
    realUrl = 'http://www.nmc.cn/f/rest/real/'

    def __init__(self,province,city):
        self.province = province
        self.city = city
        self.dataIsValid = False
        self.city_url = self.getUrl()
        self.data = []
        self.start()

    def start(self):
        threading.Thread(target=self.crawlerWeatherData).start()

    def getUrl(self):
        for i in cityDic.AllProvinceCity:
            if self.province in i['name']:
                for j in i['citys']:
                    if self.city in j['city']:
                        self.citymsgdic = j
                        return weatherCrawler.mainUrl+j['url'],weatherCrawler.apiUrl+j['code'],weatherCrawler.realUrl+j['code']
        raise ValueError

    def handleHtml(self,html):
        bs_html = bs4.BeautifulSoup(html, 'html5lib')
        html = list(list(list(bs_html.html.body.children)[5].children)[1].children)[7]
        for i in html.children:
            if not isinstance(i, bs4.NavigableString):
                for j in i.children:
                    if not isinstance(j,bs4.element.NavigableString):
                        if j['class'][0] == 'day':
                            dic = {}
                            for k in j.children:
                                if not isinstance(k, bs4.element.NavigableString):
                                    if k['class'][0] == "wicon":
                                        url = k.img['src'].replace(' ','').replace('\n','')
                                        l = url.split('/')
                                        l[-2] = 'night'
                                        url = '/'.join(l)
                                        dic[k['class'][0]] = 'pic/day/%s'%l[-1]
                                        try:
                                            file = open('pic/day/%s'%l[-1],'rb')
                                        except:
                                            urllib.request.urlretrieve(url, filename='pic/day/%s' % l[-1])
                                    else:
                                        dic[k['class'][0]] = str(k.string).replace(' ','').replace('\n','')
                            self.data.append(dic)

    def crawlerWeatherData(self):
        headers = [('Accept',' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'),
                   # ('Accept-Encoding','gzip, deflate'),
                   ('Accept-Language','zh-CN,zh;q=0.9'),
                   ('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'),
                   ('Connection','keep-alive'),
                   ('Upgrade - Insecure - Requests','1'),
                   ('Host','www.nmc.cn')]
        try:
            html = urllib.request.urlopen(self.city_url[0]).read().decode('utf-8')
            self.handleHtml(html)
            cjar = http.cookiejar.CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
            opener.addheaders = headers
            urllib.request.install_opener(opener)
            self.apiUrljson = json.loads(str(urllib.request.urlopen(self.city_url[1]).read(), encoding='utf-8'))
            self.realUrljson = json.loads(str(urllib.request.urlopen(self.city_url[2]).read(), encoding='utf-8'))
            self.dataIsValid = True
        except Exception as e:
            print(e)
            self.dataIsValid = False

    def getData(self):
        if self.dataIsValid:
            return self.data,self.apiUrljson,self.realUrljson

if __name__ == '__main__':
    w = weatherCrawler('广东','深圳')
    while not w.getData():
        pass
    print(w.getData())



