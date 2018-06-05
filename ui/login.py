# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_loginDialog(object):
    def setupUi(self, loginDialog):
        loginDialog.setObjectName("loginDialog")
        loginDialog.resize(380, 250)
        self.usernamelabel = QtWidgets.QLabel(loginDialog)
        self.usernamelabel.setGeometry(QtCore.QRect(110, 140, 54, 12))
        self.usernamelabel.setObjectName("usernamelabel")
        self.passwdlabel = QtWidgets.QLabel(loginDialog)
        self.passwdlabel.setGeometry(QtCore.QRect(120, 170, 41, 16))
        self.passwdlabel.setObjectName("passwdlabel")
        self.usernamelineEdit = QtWidgets.QLineEdit(loginDialog)
        self.usernamelineEdit.setGeometry(QtCore.QRect(150, 140, 113, 20))
        self.usernamelineEdit.setObjectName("usernamelineEdit")
        self.passwdlineEdit = QtWidgets.QLineEdit(loginDialog)
        self.passwdlineEdit.setGeometry(QtCore.QRect(150, 170, 113, 20))
        self.passwdlineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwdlineEdit.setObjectName("passwdlineEdit")
        self.loginpushButton = QtWidgets.QPushButton(loginDialog)
        self.loginpushButton.setGeometry(QtCore.QRect(120, 200, 75, 23))
        self.loginpushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.loginpushButton.setObjectName("loginpushButton")
        self.registerpushButton = QtWidgets.QPushButton(loginDialog)
        self.registerpushButton.setGeometry(QtCore.QRect(200, 200, 75, 23))
        self.registerpushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.registerpushButton.setObjectName("registerpushButton")
        self.unconnectlabel = QtWidgets.QLabel(loginDialog)
        self.unconnectlabel.setGeometry(QtCore.QRect(10, 220, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(7)
        self.unconnectlabel.setFont(font)
        self.unconnectlabel.setStyleSheet("border-image: url(source/None.png);color:rgb(255, 0, 0);font-size:15px;font-family:Microsoft YaHei;\n"
"font: 63 12pt \"Bahnschrift SemiBold\";")
        self.unconnectlabel.setTextFormat(QtCore.Qt.RichText)
        self.unconnectlabel.setObjectName("unconnectlabel")

        self.retranslateUi(loginDialog)
        QtCore.QMetaObject.connectSlotsByName(loginDialog)

    def retranslateUi(self, loginDialog):
        _translate = QtCore.QCoreApplication.translate
        loginDialog.setWindowTitle(_translate("loginDialog", "微聊-登录"))
        self.usernamelabel.setText(_translate("loginDialog", "用户名:"))
        self.passwdlabel.setText(_translate("loginDialog", "密码:"))
        self.loginpushButton.setToolTip(_translate("loginDialog", "<html><head/><body><p><span style=\" font-size:12pt; color:#00aaff;\">登录</span></p></body></html>"))
        self.loginpushButton.setText(_translate("loginDialog", "登录"))
        self.registerpushButton.setToolTip(_translate("loginDialog", "<html><head/><body><p><span style=\" font-size:12pt; color:#00aaff;\">注册</span></p></body></html>"))
        self.registerpushButton.setText(_translate("loginDialog", "注册"))
        self.unconnectlabel.setText(_translate("loginDialog", "unconnected server..."))

