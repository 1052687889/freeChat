# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_chatDlg(object):
    def setupUi(self, chatDlg):
        chatDlg.setObjectName("chatDlg")
        chatDlg.resize(477, 550)
        chatDlg.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../pic/logo.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        chatDlg.setWindowIcon(icon)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(chatDlg)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.MsgTextEdit = QtWidgets.QTextEdit(chatDlg)
        self.MsgTextEdit.setObjectName("MsgTextEdit")
        self.verticalLayout_3.addWidget(self.MsgTextEdit)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.SendtextBrowser = QtWidgets.QTextBrowser(chatDlg)
        self.SendtextBrowser.setObjectName("SendtextBrowser")
        self.horizontalLayout.addWidget(self.SendtextBrowser)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.SendButton = QtWidgets.QToolButton(chatDlg)
        self.SendButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SendButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../pic/send.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SendButton.setIcon(icon1)
        self.SendButton.setIconSize(QtCore.QSize(32, 32))
        self.SendButton.setAutoRaise(True)
        self.SendButton.setObjectName("SendButton")
        self.verticalLayout_4.addWidget(self.SendButton)
        self.historyButton = QtWidgets.QToolButton(chatDlg)
        self.historyButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.historyButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../pic/history.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.historyButton.setIcon(icon2)
        self.historyButton.setIconSize(QtCore.QSize(32, 32))
        self.historyButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.historyButton.setAutoRaise(True)
        self.historyButton.setObjectName("historyButton")
        self.verticalLayout_4.addWidget(self.historyButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 10)
        self.verticalLayout.setStretch(1, 3)
        self.verticalLayout_5.addLayout(self.verticalLayout)

        self.retranslateUi(chatDlg)
        QtCore.QMetaObject.connectSlotsByName(chatDlg)

    def retranslateUi(self, chatDlg):
        _translate = QtCore.QCoreApplication.translate
        chatDlg.setWindowTitle(_translate("chatDlg", "微聊"))
        self.MsgTextEdit.setHtml(_translate("chatDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.SendButton.setToolTip(_translate("chatDlg", "<html><head/><body><p><span style=\" font-size:12pt; color:#00aaff;\">发送</span></p></body></html>"))
        self.historyButton.setToolTip(_translate("chatDlg", "<html><head/><body><p><span style=\" font-size:12pt; color:#00aaff;\">历史记录</span></p></body></html>"))

