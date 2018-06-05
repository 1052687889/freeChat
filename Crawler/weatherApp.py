#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
# Author:taoke
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *

class weatherApp(QMainWindow):
    htmlPath = 'weather.html'
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("天气情况")
        self.setWindowIcon(QIcon('weatherlogo.jpg'))
        self.showMaximized()
        self.show()

    def display(self):
        self.browser = QWebEngineView()
        with open('weather.html','r',encoding='utf-8') as file:
            s = file.read()
            print(s)

        self.browser.setHtml(s)
        self.setCentralWidget(self.browser)


if __name__=='__main__':
    app = QApplication(sys.argv)
    window = weatherApp()
    window.display()
    window.show()
    sys.exit(app.exec_())









