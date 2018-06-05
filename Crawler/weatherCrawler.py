#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
# Author:taoke
import re
import urllib.request
import cityDic
import threading
import json
import http.cookiejar
import weatherApp
from PyQt5.QtWidgets import *
import sys
import pathlib
import time
import PyQt5
class ipAddrAreaCrawler(object):
    url = 'http://2018.ip138.com/ic.asp'
    ipAddrArea = ()
    def __init__(self):
        self.ip = ''       #IP
        self.province = '' #省
        self.city = ''     #城市
        self.operator = '' #运营商
        threading.Thread(target=self.startCrawler).start()

    def startCrawler(self):
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

    def getipAddArea(self):
        return ipAddrAreaCrawler.ipAddrArea

class weatherCrawler(object):
    #          http://www.nmc.cn/publish/forecast/AGD/shenzhen.html
    mainUrl = 'http://www.nmc.cn'
    apiUrl =  'http://www.nmc.cn/f/rest/aqi/'
    realUrl = 'http://www.nmc.cn/f/rest/real/'
    s = {'forecasttime': '', 'aqi': '', 'aq': 9999, 'text': '-', 'aqiCode': ''}
    z = {'station': {'url': '/publish/forecast/AGD/shenzhen.html', 'code': '59493', 'city': '深圳', 'province': '广东省'}, 'publish_time': '2018-05-28 20:35', 'weather': {'temperature': 29.7, 'temperatureDiff': 0.5, 'airpressure': 1002.0, 'humidity': 66.0, 'rain': 0.0, 'rcomfort': 76, 'icomfort': 2, 'info': '多云', 'img': '1', 'feelst': 29.2}, 'wind': {'direct': '西南风', 'power': '微风', 'speed': 1.3}, 'warn': {'alert': '9999', 'pic': '9999', 'province': '9999', 'city': '9999', 'url': '9999', 'issuecontent': '9999', 'fmeans': '9999'}}

    def __init__(self,province,city):
        self.province = province
        self.city = city
        self.dataIsValid = False
        self.city_url = self.getUrl()
        # threading.Thread(target=self.getWeatherData)

    def getUrl(self):
        for i in cityDic.AllProvinceCity:
            if self.province in i['name']:
                for j in i['citys']:
                    if self.city in j['city']:
                        self.citymsgdic = j
                        return weatherCrawler.mainUrl+j['url'],weatherCrawler.apiUrl+j['code'],weatherCrawler.realUrl+j['code']
        raise ValueError

    def handleHtml(self,html):
        pass

    def getHtml(self):
        return self.mainUrlhtml

    def updataLocalHtml(self):

        print(self.mainUrlhtml)
        return self.mainUrlhtml

    def getWeatherData(self):
        headers = [('Accept',' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'),
                   ('Accept-Encoding','gzip, deflate'),
                   ('Accept-Language','zh-CN,zh;q=0.9'),
                   ('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'),
                   ('Connection','keep-alive'),
                   ('Upgrade - Insecure - Requests','1'),
                   ('Host','www.nmc.cn')]
        # while True:
        self.mainUrlhtml = str(urllib.request.urlopen(self.city_url[0]).read(), encoding='utf-8')
        cjar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
        opener.addheaders = headers
        urllib.request.install_opener(opener)
        self.apiUrljson = json.loads(str(urllib.request.urlopen(self.city_url[1]).read(), encoding='utf-8'))
        self.realUrljson = json.loads(str(urllib.request.urlopen(self.city_url[2]).read(), encoding='utf-8'))
        self.dataIsValid = True
        print(self.apiUrljson,'\r\n', self.realUrljson)
        # time.sleep(60*5)
        # data = str(urllib.request.urlopen(self.city_url[0]).read(),encoding='utf-8')
        # with open('2.html','w',encoding='utf-8') as file1:
        #     file1.write(self.mainUrlhtml)


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # window = weatherApp.weatherApp()
    # window.display()
    # window.show()
    # sys.exit(app.exec_())

    w = weatherCrawler('广东','深圳')
    w.getWeatherData()




