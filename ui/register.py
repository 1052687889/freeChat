# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_registerDialog(object):
    def setupUi(self, registerDialog):
        registerDialog.setObjectName("registerDialog")
        registerDialog.resize(380, 250)
        registerDialog.setMinimumSize(QtCore.QSize(380, 250))
        registerDialog.setMaximumSize(QtCore.QSize(380, 250))
        self.returnpushButton = QtWidgets.QPushButton(registerDialog)
        self.returnpushButton.setGeometry(QtCore.QRect(220, 200, 75, 23))
        self.returnpushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.returnpushButton.setObjectName("returnpushButton")
        self.usernamelabel = QtWidgets.QLabel(registerDialog)
        self.usernamelabel.setGeometry(QtCore.QRect(110, 110, 41, 16))
        self.usernamelabel.setObjectName("usernamelabel")
        self.passwdlabel = QtWidgets.QLabel(registerDialog)
        self.passwdlabel.setGeometry(QtCore.QRect(120, 140, 31, 16))
        self.passwdlabel.setObjectName("passwdlabel")
        self.passwdsurelabel = QtWidgets.QLabel(registerDialog)
        self.passwdsurelabel.setGeometry(QtCore.QRect(100, 170, 54, 12))
        self.passwdsurelabel.setObjectName("passwdsurelabel")
        self.usernamelineEdit = QtWidgets.QLineEdit(registerDialog)
        self.usernamelineEdit.setGeometry(QtCore.QRect(160, 110, 113, 20))
        self.usernamelineEdit.setObjectName("usernamelineEdit")
        self.passwdlineEdit = QtWidgets.QLineEdit(registerDialog)
        self.passwdlineEdit.setGeometry(QtCore.QRect(160, 140, 113, 20))
        self.passwdlineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwdlineEdit.setObjectName("passwdlineEdit")
        self.passwdsurelineEdit = QtWidgets.QLineEdit(registerDialog)
        self.passwdsurelineEdit.setGeometry(QtCore.QRect(160, 170, 113, 20))
        self.passwdsurelineEdit.setText("")
        self.passwdsurelineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwdsurelineEdit.setObjectName("passwdsurelineEdit")
        self.registerpushButton = QtWidgets.QPushButton(registerDialog)
        self.registerpushButton.setGeometry(QtCore.QRect(130, 200, 75, 23))
        self.registerpushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.registerpushButton.setObjectName("registerpushButton")
        self.unconnectlabel = QtWidgets.QLabel(registerDialog)
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

        self.retranslateUi(registerDialog)
        QtCore.QMetaObject.connectSlotsByName(registerDialog)

    def retranslateUi(self, registerDialog):
        _translate = QtCore.QCoreApplication.translate
        registerDialog.setWindowTitle(_translate("registerDialog", "微聊-注册"))
        self.returnpushButton.setToolTip(_translate("registerDialog", "<html><head/><body><p><span style=\" font-size:12pt; color:#00aaff;\">返回</span></p></body></html>"))
        self.returnpushButton.setText(_translate("registerDialog", "返回"))
        self.usernamelabel.setText(_translate("registerDialog", "用户名:"))
        self.passwdlabel.setText(_translate("registerDialog", "密码:"))
        self.passwdsurelabel.setText(_translate("registerDialog", "确认密码:"))
        self.registerpushButton.setToolTip(_translate("registerDialog", "<html><head/><body><p><span style=\" font-size:12pt; color:#00aaff;\">注册</span></p></body></html>"))
        self.registerpushButton.setText(_translate("registerDialog", "注册"))
        self.unconnectlabel.setText(_translate("registerDialog", "unconnected server..."))

