# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'adduser.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_adduserDialog(object):
    def setupUi(self, adduserDialog):
        adduserDialog.setObjectName("adduserDialog")
        adduserDialog.resize(200, 130)
        adduserDialog.setMinimumSize(QtCore.QSize(200, 130))
        adduserDialog.setMaximumSize(QtCore.QSize(200, 130))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pic/logo.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        adduserDialog.setWindowIcon(icon)
        self.usernamelabel = QtWidgets.QLabel(adduserDialog)
        self.usernamelabel.setGeometry(QtCore.QRect(15, 32, 54, 12))
        self.usernamelabel.setObjectName("usernamelabel")
        self.usernamelineEdit = QtWidgets.QLineEdit(adduserDialog)
        self.usernamelineEdit.setGeometry(QtCore.QRect(60, 30, 113, 20))
        self.usernamelineEdit.setObjectName("usernamelineEdit")
        self.grouplabel = QtWidgets.QLabel(adduserDialog)
        self.grouplabel.setGeometry(QtCore.QRect(27, 61, 31, 16))
        self.grouplabel.setObjectName("grouplabel")
        self.groupcomboBox = QtWidgets.QComboBox(adduserDialog)
        self.groupcomboBox.setGeometry(QtCore.QRect(60, 60, 111, 22))
        self.groupcomboBox.setObjectName("groupcomboBox")
        self.adduserButton = QtWidgets.QToolButton(adduserDialog)
        self.adduserButton.setGeometry(QtCore.QRect(90, 90, 31, 31))
        self.adduserButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("pic/adduser.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.adduserButton.setIcon(icon1)
        self.adduserButton.setIconSize(QtCore.QSize(32, 32))
        self.adduserButton.setAutoRaise(True)
        self.adduserButton.setObjectName("adduserButton")

        self.retranslateUi(adduserDialog)
        QtCore.QMetaObject.connectSlotsByName(adduserDialog)

    def retranslateUi(self, adduserDialog):
        _translate = QtCore.QCoreApplication.translate
        adduserDialog.setWindowTitle(_translate("adduserDialog", "添加好友"))
        self.usernamelabel.setText(_translate("adduserDialog", "用户名:"))
        self.usernamelineEdit.setToolTip(_translate("adduserDialog", "<html><head/><body><p><span style=\" font-size:12pt; color:#00aaff;\">用户名</span></p></body></html>"))
        self.grouplabel.setText(_translate("adduserDialog", "分组:"))
        self.groupcomboBox.setToolTip(_translate("adduserDialog", "<html><head/><body><p><span style=\" font-size:12pt; color:#00aaff;\">选择分组</span></p></body></html>"))
        self.adduserButton.setToolTip(_translate("adduserDialog", "<html><head/><body><p>添加用户</p></body></html>"))

