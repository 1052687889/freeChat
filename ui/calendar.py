# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calendar.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_calendarDlg(object):
    def setupUi(self, calendarDlg):
        calendarDlg.setObjectName("calendarDlg")
        calendarDlg.resize(237, 217)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pic/calendar.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        calendarDlg.setWindowIcon(icon)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(calendarDlg)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.calendarWidget = QtWidgets.QCalendarWidget(calendarDlg)
        self.calendarWidget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.calendarWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.calendarWidget.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.calendarWidget.setMaximumDate(QtCore.QDate(2099, 12, 31))
        self.calendarWidget.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setObjectName("calendarWidget")
        self.verticalLayout.addWidget(self.calendarWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(calendarDlg)
        QtCore.QMetaObject.connectSlotsByName(calendarDlg)

    def retranslateUi(self, calendarDlg):
        _translate = QtCore.QCoreApplication.translate
        calendarDlg.setWindowTitle(_translate("calendarDlg", "日历"))

