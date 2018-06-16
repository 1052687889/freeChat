# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'snake_config_view.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys,os
from const import *
class Ui_snake_config(object):

    def __init__(self, p1,queue):
        super().__init__()
        self.p1 = p1
        self.config_all = {}
        self.queue = queue
        self.snake_config = None

    def setupUi(self, snake_config):
        self.snake_config = snake_config
        snake_config.setObjectName("snake_config")
        snake_config.resize(461, 466)
        snake_config.setStyleSheet("background-color: rgb(220, 220, 220);")
        self.label_3 = QtWidgets.QLabel(snake_config)
        self.label_3.setGeometry(QtCore.QRect(70, 120, 71, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(snake_config)
        self.label_4.setGeometry(QtCore.QRect(80, 360, 54, 12))
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(snake_config)
        self.label.setGeometry(QtCore.QRect(90, 40, 54, 12))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(snake_config)
        self.label_2.setGeometry(QtCore.QRect(43, 320, 91, 20))
        self.label_2.setObjectName("label_2")
        self.exit_game = QtWidgets.QPushButton(snake_config)
        self.exit_game.setGeometry(QtCore.QRect(310, 420, 75, 23))
        self.exit_game.setObjectName("exit_game")
        self.exit_game.clicked.connect(self.exit_game_func)

        self.start_game = QtWidgets.QPushButton(snake_config)
        self.start_game.setGeometry(QtCore.QRect(60, 420, 75, 23))
        self.start_game.setObjectName("start_game")
        self.start_game.clicked.connect(self.start_game_func)

        self.game_class = QtWidgets.QSpinBox(snake_config)
        self.game_class.setGeometry(QtCore.QRect(220, 360, 111, 22))
        self.game_class.setMinimum(1)
        self.game_class.setMaximum(9)
        self.game_class.setObjectName("game_class")
        self.food_number = QtWidgets.QSpinBox(snake_config)
        self.food_number.setGeometry(QtCore.QRect(220, 120, 111, 22))
        self.food_number.setMinimum(1)
        self.food_number.setMaximum(100)
        self.food_number.setObjectName("food_number")
        self.food_number.setValue(5)

        self.snake_length = QtWidgets.QSpinBox(snake_config)
        self.snake_length.setGeometry(QtCore.QRect(220, 320, 111, 22))
        self.snake_length.setMinimum(1)
        self.snake_length.setMaximum(10)
        self.snake_length.setObjectName("snake_length")
        self.speed = QtWidgets.QDoubleSpinBox(snake_config)
        self.speed.setGeometry(QtCore.QRect(220, 40, 111, 22))
        self.speed.setMinimum(0.01)
        self.speed.setMaximum(1.0)
        self.speed.setSingleStep(0.01)
        self.speed.setValue(0.15)
        self.speed.setObjectName("speed")

        self.label_5 = QtWidgets.QLabel(snake_config)
        self.label_5.setGeometry(QtCore.QRect(70, 80, 91, 16))
        self.label_5.setObjectName("label_5")

        self.speed_distance = QtWidgets.QSpinBox(snake_config)
        self.speed_distance.setGeometry(QtCore.QRect(220, 80, 111, 22))
        self.speed_distance.setMinimum(1)
        self.speed_distance.setMaximum(20)
        self.speed_distance.setValue(20)
        self.speed_distance.setObjectName("speed_distance")

        self.label_9 = QtWidgets.QLabel(snake_config)
        self.label_9.setGeometry(QtCore.QRect(70, 160, 71, 16))
        self.label_9.setObjectName("label_9")

        self.add_size = QtWidgets.QSpinBox(snake_config)
        self.add_size.setGeometry(QtCore.QRect(220, 160, 111, 22))
        self.add_size.setMinimum(1)
        self.add_size.setMaximum(4)
        self.add_size.setObjectName("add_size")

        self.snake_shape = QtWidgets.QGroupBox(snake_config)
        self.snake_shape.setGeometry(QtCore.QRect(40, 190, 401, 31))
        self.snake_shape.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.snake_shape.setToolTip("")
        self.snake_shape.setStyleSheet("border-color: rgb(255, 255, 255);")
        self.snake_shape.setTitle("")
        self.snake_shape.setObjectName("snake_shape")
        self.label_6 = QtWidgets.QLabel(self.snake_shape)
        self.label_6.setGeometry(QtCore.QRect(40, 10, 54, 12))
        self.label_6.setObjectName("label_6")
        self.ss_rectangle = QtWidgets.QRadioButton(self.snake_shape)
        self.ss_rectangle.setGeometry(QtCore.QRect(180, 10, 61, 16))
        self.ss_rectangle.setObjectName("ss_rectangle")

        self.ss_oval = QtWidgets.QRadioButton(self.snake_shape)
        self.ss_oval.setGeometry(QtCore.QRect(250, 10, 51, 16))
        self.ss_oval.setObjectName("ss_oval")

        self.snake_skin_type = QtWidgets.QGroupBox(snake_config)
        self.snake_skin_type.setGeometry(QtCore.QRect(40, 230, 401, 31))
        self.snake_skin_type.setTitle("")
        self.snake_skin_type.setObjectName("snake_skin_type")
        self.skt_random_color = QtWidgets.QRadioButton(self.snake_skin_type)
        self.skt_random_color.setGeometry(QtCore.QRect(310, 10, 61, 16))
        self.skt_random_color.setObjectName("skt_random_color")
        self.skt_green = QtWidgets.QRadioButton(self.snake_skin_type)
        self.skt_green.setGeometry(QtCore.QRect(250, 10, 51, 16))
        self.skt_green.setObjectName("skt_green")
        self.label_8 = QtWidgets.QLabel(self.snake_skin_type)
        self.label_8.setGeometry(QtCore.QRect(40, 10, 54, 12))
        self.label_8.setObjectName("label_8")
        self.skt_pink = QtWidgets.QRadioButton(self.snake_skin_type)
        self.skt_pink.setGeometry(QtCore.QRect(180, 10, 51, 16))
        self.skt_pink.setObjectName("skt_pink")
        self.game_background = QtWidgets.QGroupBox(snake_config)
        self.game_background.setGeometry(QtCore.QRect(40, 270, 401, 31))
        self.game_background.setTitle("")
        self.game_background.setObjectName("game_background")
        self.gb_green = QtWidgets.QRadioButton(self.game_background)
        self.gb_green.setGeometry(QtCore.QRect(310, 10, 51, 16))
        self.gb_green.setObjectName("gb_green")
        self.gb_white = QtWidgets.QRadioButton(self.game_background)
        self.gb_white.setGeometry(QtCore.QRect(180, 10, 51, 16))
        self.gb_white.setObjectName("gb_white")
        self.gb_blue = QtWidgets.QRadioButton(self.game_background)
        self.gb_blue.setGeometry(QtCore.QRect(250, 10, 51, 16))
        self.gb_blue.setObjectName("gb_blue")
        self.label_7 = QtWidgets.QLabel(self.game_background)
        self.label_7.setGeometry(QtCore.QRect(10, 10, 91, 20))
        self.label_7.setObjectName("label_7")

        self.return_game_main = QtWidgets.QPushButton(snake_config)
        self.return_game_main.setGeometry(QtCore.QRect(190, 420, 75, 23))
        self.return_game_main.setObjectName("return_game_main")
        self.return_game_main.clicked.connect(self.return_game_main_func)

        self.gb_green.raise_()
        self.gb_white.raise_()
        self.gb_blue.raise_()
        self.label_7.raise_()
        self.gb_green.raise_()
        self.gb_white.raise_()
        self.gb_blue.raise_()
        self.label_7.raise_()

        self.retranslateUi(snake_config)
        QtCore.QMetaObject.connectSlotsByName(snake_config)

    def retranslateUi(self, snake_config):
        _translate = QtCore.QCoreApplication.translate
        snake_config.setWindowTitle(_translate("snake_config", "Form"))
        self.label_3.setText(_translate("snake_config", "食物的个数"))
        self.label_4.setText(_translate("snake_config", "关卡"))
        self.label.setText(_translate("snake_config", "速度"))
        self.label_2.setText(_translate("snake_config", "长度(初始长度)"))
        self.exit_game.setText(_translate("snake_config", "退出"))
        self.start_game.setText(_translate("snake_config", "开始游戏"))
        self.label_5.setText(_translate("snake_config", "移动的距离"))
        self.label_9.setText(_translate("snake_config", "增加的长度"))
        self.label_6.setText(_translate("snake_config", "蛇的形状"))
        self.ss_rectangle.setText(_translate("snake_config", "正方形"))
        self.ss_oval.setText(_translate("snake_config", "圆形"))
        self.skt_random_color.setText(_translate("snake_config", "随机色"))
        self.skt_green.setText(_translate("snake_config", "绿色"))
        self.label_8.setText(_translate("snake_config", "皮肤样式"))
        self.skt_pink.setText(_translate("snake_config", "粉色"))
        self.gb_green.setText(_translate("snake_config", "绿色"))
        self.gb_white.setText(_translate("snake_config", "白色"))
        self.gb_blue.setText(_translate("snake_config", "蓝色"))
        self.label_7.setText(_translate("snake_config", "游戏界面背景色"))
        self.return_game_main.setText(_translate("snake_config", "返回主界面"))

    # 开始游戏
    def start_game_func(self):
        # 保存所有的配置文件
        # speed = None, speed_distance = None, food_number = None, add_size = None,
        # shape = None, skin = None, game_background = None, snake_length = None
        config_all = {"speed": None, "speed_distance": None, "food_number": None,
                      "add_size": None, "shape": None, "skin": None, "game_background": None,
                      "snake_length": None}
        # print(type(self.speed.value()))
        # 保存选择的速度
        config_all["speed"] = self.speed.value()
        # print(self.speed_distance.value())
        # 一次移动的距离
        config_all["speed_distance"] = self.speed_distance.value()
        # print(self.food_number.value())
        # 食物的个数
        config_all["food_number"] = self.food_number.value()
        # print(self.add_size.value())
        # 吃一个食物增加的长度
        config_all["add_size"] = self.add_size.value()

        print(self.snake_shape.isCheckable())
        # print(self.ss_rectangle.isChecked())
        # print(self.ss_oval.isChecked())
        # 设置蛇的身体的形状
        if self.ss_rectangle.isChecked():
            config_all["shape"] = "rectangle"
        elif self.ss_oval.isChecked():
            config_all["shape"] = "oval"

        print(self.snake_skin_type.isChecked())
        # print(self.skt_pink.isChecked())
        # print(self.skt_green.isChecked())
        # print(self.skt_random_color.isChecked())
        # 设置蛇的皮肤的样式
        if self.skt_pink.isChecked():
            config_all["skin"] = "pink"
        elif self.skt_green.isChecked():
            config_all["skin"] = "green"
        elif self.skt_random_color.isChecked():
            config_all["skin"] = "random_color"

        print(self.game_background.isChecked())
        # print(self.gb_blue.isChecked())
        # print(self.gb_green.isChecked())
        # print(self.gb_white.isChecked())
        # 设置游戏界面的颜色
        if self.gb_blue.isChecked():
            config_all["game_background"] = "blue"
        elif self.gb_green.isChecked():
            config_all["game_background"] = "green"
        elif self.gb_white.isChecked():
            config_all["game_background"] = "white"

        # 设置蛇的初始长度
        config_all["snake_length"] = self.snake_length.value()

        self.p1.send(config_all)
        # print("数据发送中")

        self.config_all = config_all
        print(config_all)
        self.snake_config.close()
        # sys.exit()

        # return config_all

    def return_game_main_func(self):
        print("返回游戏主界面")
        self.p1.send("return_game_main")
        # 关闭该窗口
        self.snake_config.close()

    def exit_game_func(self):
        print("退出游戏")
        msg = MsgType(type=MsgType.MSG_SNACK, msgtype=MsgType.CLOSE_DLG, msg=os.getpid())
        self.queue.put(msg)
        # self.snake_config.hide()
        sys.exit()


def main(p1,queue):
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_snake_config(p1,queue)
    ui.setupUi(MainWindow)
    # ui.test()
    MainWindow.show()
    app.exec_()
    ui.p1.send("exit_game")
    # sys.exit()
    # sys.exit(app.exec_())
    # print(ui.config_all)