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
        chatDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        chatDlg.resize(492, 571)
        chatDlg.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        chatDlg.setFocusPolicy(QtCore.Qt.NoFocus)
        chatDlg.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/HY-PC/.designer/pic/logo.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        chatDlg.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(chatDlg)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(chatDlg)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.line = QtWidgets.QFrame(chatDlg)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sendTextEdit = QtWidgets.QTextEdit(chatDlg)
        self.sendTextEdit.setObjectName("sendTextEdit")
        self.horizontalLayout.addWidget(self.sendTextEdit)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.fontButton = QtWidgets.QToolButton(chatDlg)
        self.fontButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:/Users/HY-PC/.designer/backup/pic/font.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fontButton.setIcon(icon1)
        self.fontButton.setIconSize(QtCore.QSize(32, 32))
        self.fontButton.setAutoRaise(True)
        self.fontButton.setObjectName("fontButton")
        self.verticalLayout_2.addWidget(self.fontButton)
        self.colorButton = QtWidgets.QToolButton(chatDlg)
        self.colorButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("C:/Users/HY-PC/.designer/backup/pic/colours.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.colorButton.setIcon(icon2)
        self.colorButton.setIconSize(QtCore.QSize(32, 32))
        self.colorButton.setAutoRaise(True)
        self.colorButton.setObjectName("colorButton")
        self.verticalLayout_2.addWidget(self.colorButton)
        self.SendButton = QtWidgets.QToolButton(chatDlg)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.SendButton.setFont(font)
        self.SendButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SendButton.setMouseTracking(True)
        self.SendButton.setTabletTracking(True)
        self.SendButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("C:/Users/HY-PC/.designer/backup/pic/send.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SendButton.setIcon(icon3)
        self.SendButton.setIconSize(QtCore.QSize(32, 32))
        self.SendButton.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.SendButton.setAutoRaise(True)
        self.SendButton.setObjectName("SendButton")
        self.verticalLayout_2.addWidget(self.SendButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 6)
        self.verticalLayout.setStretch(2, 2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(chatDlg)
        QtCore.QMetaObject.connectSlotsByName(chatDlg)

    def retranslateUi(self, chatDlg):
        _translate = QtCore.QCoreApplication.translate
        chatDlg.setWindowTitle(_translate("chatDlg", "微聊"))
        self.textBrowser.setHtml(_translate("chatDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.sendTextEdit.setHtml(_translate("chatDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:20pt;\"><br /></p></body></html>"))
        self.fontButton.setToolTip(_translate("chatDlg", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#00aaff;\">设置字体</span></p></body></html>"))
        self.colorButton.setToolTip(_translate("chatDlg", "<html><head/><body><p><span style=\" font-size:12pt; color:#00aaff;\">设置颜色</span></p></body></html>"))
        self.SendButton.setToolTip(_translate("chatDlg", "<html><head/><body><p><span style=\" font-size:12pt; color:#00aaff;\">发送</span></p></body></html>"))

