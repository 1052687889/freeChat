#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
# Author:taoke
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class basis(object):
    @staticmethod
    def setBackPic(dlg,str):
        window_pale = QtGui.QPalette()
        window_pale.setBrush(dlg.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(str)))
        dlg.setPalette(window_pale)

    @staticmethod
    def center(dlg):
        # 获得窗口
        qr = dlg.frameGeometry()
        # 获得屏幕中心点
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        dlg.move(qr.topLeft())

class Communicate(QtCore.QObject):
    closeApp = QtCore.pyqtSignal()

import login
import register

class registerLoginDlg(object):
    def __init__(self):
        self.loginDlg = login.loginDialog(self.loginDlgClickLogin,self.loginDlgClickRegister)
        self.loginDlg.show()
        self.rgisterDlg = register.registerDialog(self.registerDlgClickRegister,self.registerDlgClickReturn)
        self.rgisterDlg.hide()

    def loginDlgClickLogin(self):
        print('_____________---')
        pass

    def loginDlgClickRegister(self):
        self.loginDlg.hide()
        self.rgisterDlg.show()
        basis.center(self.loginDlg)

    def registerDlgClickRegister(self):
        print('_____________---')

    def registerDlgClickReturn(self):
        self.loginDlg.show()
        self.rgisterDlg.hide()
        basis.center(self.rgisterDlg)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = registerLoginDlg()
    sys.exit(app.exec_())















