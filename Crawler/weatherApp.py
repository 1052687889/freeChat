#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
# Author:taoke
'''
本工程为天气查询系统，可以查询中国的各个城市未来七天的天气情况
原理：通过request请求模拟浏览器获取中央气象网的数据，通过textBo
'''

import sys,pathlib,threading,queue,os
import weather
import bs4
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cityDic,weatherCrawler
from const import *
class weatherDlg(weather.Ui_weatherDlg,QWidget):
    def __init__(self,send_queue,parent=None):
        self.threadList = []
        super(weatherDlg, self).__init__(parent)
        self.msg_queue = queue.Queue()
        self.send_queue = send_queue
        self.setupUi(self)
        self.init_Ui()
        self.show()
        self.ipAddrCrawler = weatherCrawler.ipAddrAreaCrawler()
        self.timer = QTimer()
        self.timer.timeout.connect(self.handleMsg)
        self.timer.start(20)

    def init_Ui(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(str(pathlib.Path(__file__).parent/"pic/query.jpg")), QIcon.Normal, QIcon.Off)
        self.queryButton.setIcon(icon)
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(str(pathlib.Path(__file__).parent/"pic/currentcity.ico")), QIcon.Normal, QIcon.Off)
        self.curentCityButton.setIcon(icon1)
        self.setBackPic(self,str(pathlib.Path(__file__).parent/"pic/backpic.bmp"))
        self.setWindowIcon(QIcon(str(pathlib.Path(__file__).parent / "pic" / "weatherlogo.jpg")))
        self.center(self)
        self.setWindowTitle('微聊-天气查询')
        self.provinceComboBox.addItems((province['name'] for province in cityDic.AllProvinceCity))
        self.provinceComboBox.activated.connect(self.provinceComboBox_activated)
        self.queryButton.clicked.connect(self.queryButton_clicked)
        self.curentCityButton.clicked.connect(self.currentCityButton_clicked)
        self.textBrowser.setHtml('<h1 style="color: #1c94c4">使用说明<\h1>\
                                    <p style="color: #1c94c4;font-weight: 900" align="left">1、选择想要查询的城市，点击查询按钮查询天气<\p>\
                                    <p style="color: #1c94c4;font-weight: 900" align="left">2、点击当前城市按钮，自动选择当前所在城市<\p>')
        self.resize(880, 550)
        self.setFixedSize(880, 550)

    def provinceComboBox_activated(self):
        print('provinceComboBox_activated',self.provinceComboBox.currentText())
        for province in cityDic.AllProvinceCity:
            if province['name'] == (self.provinceComboBox.currentText()):
                print(province['name'] ,self.provinceComboBox.currentText(),province['citys'])
                self.cityComboBox.clear()
                print('---------->')
                print([city['city'] for city in province['citys']])
                self.cityComboBox.addItems((city['city'] for city in province['citys']))

    def handleMsg(self):
            if not self.msg_queue.empty():
                msg = self.msg_queue.get()
                if msg == 'crawler_data_ready':
                    self.updata_to_html()
                    self.crawler = None

            if self.iplabel.text() == '':
                ip = self.ipAddrCrawler.getipAddArea()
                if ip:
                    self.iplabel.setText('当前城市:  '+ip[1]+ip[2]+'  '+ip[3]+' ip地址:'+ip[0])
                    for province in cityDic.AllProvinceCity:
                        if province['name'].find(ip[1])>=0:
                            self.provinceComboBox.setCurrentText(province['name'])
                            self.cityComboBox.addItems((city['city'] for city in province['citys']))
                            for city in province['citys']:
                                if city['city'].find(ip[2]) >= 0:
                                    self.cityComboBox.setCurrentText(city['city'])

    def find_city_data(self,province,city):
        for p in cityDic.AllProvinceCity:
            if p['name'] == province:
                for c in p['citys']:
                    if c['city'] == city:
                        return c
        return None

    def check_crawler_data(self):
        while True:
            if self.crawler.getData():
                print(self.crawler.getData())
                # print('check_crawler_data -- self.threadList:', self.threadList)
                self.threadList.remove('check_crawler_data_threading')
                # print('check_crawler_data -- self.threadList:', self.threadList)
                self.msg_queue.put('crawler_data_ready')
                break

    def handle_html(self,html):
        data = self.crawler.getData()
        bs_html = bs4.BeautifulSoup(html, 'html5lib')
        try:
            bs_html.html.body.contents[1].string = str(bs_html.html.body.contents[1].string)+ \
                                                   data[2]['publish_time']+\
                                                   data[2]['station']['province']+\
                                                   data[2]['station']['city']+' - '+data[2]['station']['code']

            bs_html.html.body.contents[3].tbody.contents[0].contents[3].string = str('-' if data[2]['weather']['temperature'] == 9999 else data[2]['weather']['temperature'])+'℃'
            bs_html.html.body.contents[3].tbody.contents[0].contents[7].string = str('-' if data[2]['weather']['rain'] == 9999 else data[2]['weather']['rain'])+'mm' #power
            bs_html.html.body.contents[3].tbody.contents[0].contents[11].string = '-' if '9999' == str(data[2]['wind']['direct'])else  str(data[2]['wind']['direct'])+str(data[2]['wind']['power'])

            bs_html.html.body.contents[3].tbody.contents[2].contents[3].string = str('-' if data[1]['text'] == '9999' else data[1]['text'])
            bs_html.html.body.contents[3].tbody.contents[2].contents[7].string = str('-' if data[2]['weather']['humidity'] == 9999 else data[2]['weather']['humidity'])+'%'
            bs_html.html.body.contents[3].tbody.contents[2].contents[11].string = str('-'if data[2]['weather']['feelst'] == 9999 else data[2]['weather']['feelst']) + '℃'
        except:
            print('data error')
        # print(bs_html.prettify())
        # print(__file__)
        for i in range(7):
            bs_html.html.body.contents[7].tbody.contents[0].contents[1+i*2].contents[1].string = data[0][i]['date']
            bs_html.html.body.contents[7].tbody.contents[0].contents[1+i*2].contents[3].string = data[0][i]['week']
            bs_html.html.body.contents[7].tbody.contents[0].contents[1+i*2].contents[5]['src'] = 'Crawler/'+data[0][i]['wicon']
            bs_html.html.body.contents[7].tbody.contents[0].contents[1+i*2].contents[7].string = data[0][i]['wdesc']
            bs_html.html.body.contents[7].tbody.contents[0].contents[1+i*2].contents[9].string = data[0][i]['temp']
            bs_html.html.body.contents[7].tbody.contents[0].contents[1+i*2].contents[11].string = data[0][i]['direct']
            bs_html.html.body.contents[7].tbody.contents[0].contents[1+i*2].contents[13].string = data[0][i]['wind']

        return bs_html.prettify()

    def updata_to_html(self):
        path = str(pathlib.Path(__file__).parent / 'weather.html')
        with open(path,'rb') as file:
            html = file.read().decode()
            self.textBrowser.setHtml(self.handle_html(html))

    def queryButton_clicked(self):
        province = self.provinceComboBox.currentText()
        city = self.cityComboBox.currentText()
        self.crawler = weatherCrawler.weatherCrawler(province,city)
        if 'check_crawler_data_threading' not in self.threadList:
            self.textBrowser.setHtml('<h1 style="color: #1c94c4">查询中。。。<\h1>')
            threading.Thread(target=self.check_crawler_data).start()
            self.threadList.append('check_crawler_data_threading')


    def currentCityButton_clicked(self):
        self.iplabel.setText('')

    def closeEvent(self, QCloseEvent):
        msg = MsgType(type=MsgType.MSG_WEATHER,msgtype=MsgType.CLOSE_DLG,msg = os.getpid())
        self.send_queue.put(msg)

    @staticmethod
    def setBackPic(dlg,str):
        window_pale = QPalette()
        window_pale.setBrush(dlg.backgroundRole(), QBrush(QPixmap(str)))
        dlg.setPalette(window_pale)

    @staticmethod
    def center(dlg):
        # 获得窗口
        qr = dlg.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        dlg.move(qr.topLeft())

def main(queue):
    app = QApplication(sys.argv)
    window = weatherDlg(queue)
    sys.exit(app.exec_())

if __name__=='__main__':
    q = queue.Queue()
    app = QApplication(sys.argv)
    window = weatherDlg(q)
    sys.exit(app.exec_())









