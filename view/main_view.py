# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_view.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys,os
from const import *

class Ui_Snake_main(object):

    def __init__(self, p1,queue):
        super().__init__()
        self.p1 = p1
        self.Snake_main = None
        self.queue = queue

    def setupUi(self, Snake_main):
        self.Snake_main = Snake_main
        Snake_main.setObjectName("Snake_main")
        Snake_main.resize(400, 281)
        self.start_game = QtWidgets.QPushButton(Snake_main)
        self.start_game.setGeometry(QtCore.QRect(30, 230, 75, 23))
        self.start_game.setObjectName("start_game")
        self.start_game.clicked.connect(self.start_game_func)

        self.label = QtWidgets.QLabel(Snake_main)
        self.label.setGeometry(QtCore.QRect(70, 50, 211, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Snake_main)
        self.label_2.setGeometry(QtCore.QRect(70, 90, 181, 16))
        self.label_2.setObjectName("label_2")

        self.config_start_game = QtWidgets.QPushButton(Snake_main)
        self.config_start_game.setGeometry(QtCore.QRect(160, 230, 75, 23))
        self.config_start_game.setObjectName("config_start_game")
        self.config_start_game.clicked.connect(self.config_start_game_func)

        self.exit_game = QtWidgets.QPushButton(Snake_main)
        self.exit_game.setGeometry(QtCore.QRect(290, 230, 75, 23))
        self.exit_game.setObjectName("exit_game")
        self.exit_game.clicked.connect(self.exit_game_func)

        self.label_3 = QtWidgets.QLabel(Snake_main)
        self.label_3.setGeometry(QtCore.QRect(30, 20, 41, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Snake_main)
        self.label_4.setGeometry(QtCore.QRect(30, 140, 54, 12))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Snake_main)
        self.label_5.setGeometry(QtCore.QRect(70, 170, 251, 16))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Snake_main)
        QtCore.QMetaObject.connectSlotsByName(Snake_main)

    def retranslateUi(self, Snake_main):
        _translate = QtCore.QCoreApplication.translate
        Snake_main.setWindowTitle(_translate("Snake_main", "Form"))
        self.start_game.setText(_translate("Snake_main", "开始游戏"))
        self.label.setText(_translate("Snake_main", "开始游戏：表示使用默认属性开始游戏"))
        self.label_2.setText(_translate("Snake_main", "自定义游戏：自定义属性开始游戏"))
        self.config_start_game.setText(_translate("Snake_main", "自定义游戏"))
        self.exit_game.setText(_translate("Snake_main", "退出游戏"))
        self.label_3.setText(_translate("Snake_main", "解释："))
        self.label_4.setText(_translate("Snake_main", "注意："))
        self.label_5.setText(_translate("Snake_main", "自定义的属性是临时设置的， 下次再玩会重置"))

    # 开始游戏
    def start_game_func(self):
        self.p1.send("start")
        self.Snake_main.close()

    # 进入设置游戏属性界面
    def config_start_game_func(self):
        self.p1.send("config_start")
        self.Snake_main.close()

    # 退出游戏
    def exit_game_func(self):
        # print("退出游戏")
        msg = MsgType(type=MsgType.MSG_SNACK, msgtype=MsgType.CLOSE_DLG, msg=os.getpid())
        self.queue.put(msg)
        sys.exit()


def main(p1,queue):
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Snake_main(p1,queue)
    ui.setupUi(MainWindow)
    # ui.test()
    MainWindow.show()
    app.exec_()
    ui.p1.send("exit_game")
    # sys.exit(app.exec_())
    # print(ui.config_all)