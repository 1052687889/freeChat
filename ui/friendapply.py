# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'friendapply.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_applyDialog(object):
    def setupUi(self, applyDialog):
        applyDialog.setObjectName("applyDialog")
        applyDialog.resize(200, 110)
        applyDialog.setMinimumSize(QtCore.QSize(200, 110))
        applyDialog.setMaximumSize(QtCore.QSize(200, 110))
        self.agreeButton = QtWidgets.QPushButton(applyDialog)
        self.agreeButton.setGeometry(QtCore.QRect(20, 80, 75, 23))
        self.agreeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.agreeButton.setObjectName("agreeButton")
        self.refuseButton = QtWidgets.QPushButton(applyDialog)
        self.refuseButton.setGeometry(QtCore.QRect(110, 80, 75, 23))
        self.refuseButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.refuseButton.setObjectName("refuseButton")
        self.groupcomboBox = QtWidgets.QComboBox(applyDialog)
        self.groupcomboBox.setGeometry(QtCore.QRect(40, 40, 131, 22))
        self.groupcomboBox.setEditable(True)
        self.groupcomboBox.setObjectName("groupcomboBox")
        self.label = QtWidgets.QLabel(applyDialog)
        self.label.setGeometry(QtCore.QRect(10, 40, 31, 16))
        self.label.setObjectName("label")
        self.msglabel = QtWidgets.QLabel(applyDialog)
        self.msglabel.setGeometry(QtCore.QRect(40, 10, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.msglabel.setFont(font)
        self.msglabel.setObjectName("msglabel")

        self.retranslateUi(applyDialog)
        QtCore.QMetaObject.connectSlotsByName(applyDialog)

    def retranslateUi(self, applyDialog):
        _translate = QtCore.QCoreApplication.translate
        applyDialog.setWindowTitle(_translate("applyDialog", "好友申请"))
        self.agreeButton.setText(_translate("applyDialog", "同意"))
        self.refuseButton.setText(_translate("applyDialog", "拒绝"))
        self.label.setText(_translate("applyDialog", "分组"))
        self.msglabel.setText(_translate("applyDialog", "TextLabel"))

