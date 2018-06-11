#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
# Author:taoke
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont,QColor
import sys,pathlib,json,os,time,pickle
import chat,basis,login,register,friendList,adduser,_calendar
from queue import Queue
import pygame,bs4
from const import MsgType
class chatDlg(QtWidgets.QWidget,chat.Ui_chatDlg,basis.basis):
    def __init__(self,parent = None):
        super(chatDlg, self).__init__(parent)
        self.setupUi(self)
        self.init_Ui()

    def init_Ui(self):
        path = pathlib.Path(__file__)
        self.setWindowIcon(QtGui.QIcon(str(path.parent/"pic"/"logo.jpg")))
        self.resize(433, 433)
        self.setFixedSize(433, 433)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.center(self)
        self.setBackPic(self, str(path.parent/"pic"/"backpic.jpg"))

class loginDlg(QtWidgets.QWidget,login.Ui_loginDialog,basis.basis):
    def __init__(self,login_button_clicked,register_button_clicked,close_event,parent=None):
        super(loginDlg,self).__init__(parent)
        self.set_backgif('登录画面1.gif')
        self.setupUi(self)
        self.init_Ui(login_button_clicked,register_button_clicked)
        self.close_event = close_event

    def init_Ui(self,login_button_clicked,register_button_clicked):
        self.resize(400, 250)
        self.setFixedSize(400, 250)
        self.setWindowIcon(QtGui.QIcon(str(pathlib.Path(__file__).parent/"pic"/"logo.jpg")))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.center(self)
        self.unconnectlabel.hide()
        self.passwdlineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.registerpushButton.clicked.connect(register_button_clicked)
        self.loginpushButton.clicked.connect(login_button_clicked)

    def set_backgif(self,filename):
        path = pathlib.Path(__file__).parent /'pic'/ filename
        print('path:',path)
        self.backgif_label = QtWidgets.QLabel(self)
        self.backgif_label.setGeometry(0, 0, 400, 250)
        self.pix = QtGui.QPixmap(str(path))
        self.backgif_label.setPixmap(self.pix)
        self.backgif_label.setScaledContents(True)
        self.backgif = QtGui.QMovie(str(path))
        self.backgif_label.setMovie(self.backgif)
        self.backgif.start()

    def closeEvent(self, QCloseEvent):
        self.close_event()
        QCloseEvent.ignore()

class registerDlg(QtWidgets.QWidget,register.Ui_registerDialog,basis.basis):
    def __init__(self,register_button_clicked,return_button_clicked,close_event,parent=None):
        super(registerDlg,self).__init__(parent)
        self.set_backgif(r'登录画面1.gif')
        self.setupUi(self)
        self.init_Ui(register_button_clicked,return_button_clicked)
        self.close_event = close_event

    def init_Ui(self,register_button_clicked,return_button_clicked):
        self.resize(400, 250)
        self.setFixedSize(400, 250)
        self.setWindowIcon(QtGui.QIcon(str(pathlib.Path(__file__).parent/"pic"/"logo.jpg")))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.center(self)
        self.unconnectlabel.hide()
        self.passwdlineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwdsurelineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.registerpushButton.clicked.connect(register_button_clicked)
        self.returnpushButton.clicked.connect(return_button_clicked)

    def set_backgif(self,filename):
        path = pathlib.Path(__file__).parent / 'pic' / filename
        self.backgif_label = QtWidgets.QLabel(self)
        self.backgif_label.setGeometry(0, 0, 400, 250)
        self.pix = QtGui.QPixmap(str(path))
        self.backgif_label.setPixmap(self.pix)
        self.backgif_label.setScaledContents(True)
        self.backgif = QtGui.QMovie(str(path))
        self.backgif_label.setMovie(self.backgif)
        self.backgif.start()

    def closeEvent(self, QCloseEvent):
        self.close_event()
        QCloseEvent.ignore()

class registerLoginDlg(object):
    def __init__(self,send_queue,rev_queue):
        self.loginDlg = loginDlg(self.loginDlgClickLogin,self.__loginDlgClickRegister,self.login_close_event)
        self.loginDlg.show()
        self.registerDlg = registerDlg(self.registerDlgClickRegister,self.__registerDlgClickReturn,self.register_close_event)
        self.registerDlg.hide()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.handle_rev_queue)
        self.timer.start(20)
        self.send_queue = send_queue
        self.rev_queue = rev_queue
        self.in_queue = Queue(10)

    def handle_rev_queue(self):
        if not self.rev_queue.empty():
            msg = self.rev_queue.get()
            print('dlg:',msg)
            if msg.type == MsgType.MSG_SYS:
                if msg.msgtype == MsgType.EXIT:
                    sys.exit(msg.msg)

            elif msg.type == MsgType.MSG_SOCKET:
                if msg.msgtype == MsgType.FAILURE:
                    self.server_connect_display(True)
                else:
                    self.server_connect_display(False)
            elif msg.type == MsgType.MSG_REGISTER:
                d = {MsgType.FAILURE:'注册失败',MsgType.SUCCESS:'注册成功'}
                QtWidgets.QMessageBox.information(self.registerDlg, '提示', d[msg.msgtype], QtWidgets.QMessageBox.Ok)
            elif msg.type == MsgType.MSG_LOGIN:
                if msg.msgtype == MsgType.FAILURE:
                    QtWidgets.QMessageBox.information(self.loginDlg, '提示', '登录失败', QtWidgets.QMessageBox.Ok)
                else:
                    m = MsgType(type=MsgType.MSG_FRIENDLIST,msgtype=MsgType.USER_DATA,msg={'username': self.loginDlg.usernamelineEdit.text(), 'passwd': self.loginDlg.passwdlineEdit.text()})
                    self.send_queue.put(m)
                    QtCore.QCoreApplication.instance().quit()
                    print('登录成功')

    def loginDlgClickLogin(self):
        username = self.loginDlg.usernamelineEdit.text()
        passwd = self.loginDlg.passwdlineEdit.text()
        if username == '' or passwd == '':
            QtWidgets.QMessageBox.information(self.registerDlg, '提示', '用户名密码不能为空', QtWidgets.QMessageBox.Ok)
        else:
            msg = MsgType(type=MsgType.MSG_LOGIN,msgtype=MsgType.USER_DATA,msg = {'username':username,'passwd':passwd})
            self.send_queue.put(msg)

    def registerDlgClickRegister(self):
        username = self.registerDlg.usernamelineEdit.text()
        passwd = self.registerDlg.passwdlineEdit.text()
        passwdsure = self.registerDlg.passwdsurelineEdit.text()
        if username == '' or passwd == '' or passwdsure == '':
            QtWidgets.QMessageBox.information(self.registerDlg, '提示', '用户名密码不能为空', QtWidgets.QMessageBox.Ok)
        else:
            msg = MsgType(type=MsgType.MSG_REGISTER, msgtype=MsgType.USER_DATA,msg={'username': username, 'passwd': passwd})
            self.send_queue.put(msg)

    def server_connect_display(self,state):
        if state == True:
            self.loginDlg.unconnectlabel.show()
            self.registerDlg.unconnectlabel.show()
        else:
            self.loginDlg.unconnectlabel.hide()
            self.registerDlg.unconnectlabel.hide()

    def login_close_event(self):
        msg_dict = MsgType(type=MsgType.MSG_LOGIN,msgtype=MsgType.CLOSE_DLG)
        self.send_queue.put(msg_dict)

    def register_close_event(self):
        msg_dict = MsgType(type=MsgType.MSG_REGISTER, msgtype=MsgType.CLOSE_DLG)
        self.send_queue.put(msg_dict)

    def __loginDlgClickRegister(self):
        self.loginDlg.hide()
        self.registerDlg.show()
        basis.basis.center(self.loginDlg)

    def __registerDlgClickReturn(self):
        self.loginDlg.show()
        self.registerDlg.hide()
        basis.basis.center(self.registerDlg)

class friendListDlg(QtWidgets.QWidget,friendList.Ui_friendListDlg,basis.basis):

    def __init__(self,send_queue,rev_queue,parent=None):
        super(friendListDlg, self).__init__(parent)
        pygame.init()
        self.setupUi(self)
        self.init_Ui()
        self.dlgstate = []
        self.show()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.handle_rev_queue)
        self.timer.start(20)
        self.friendTreeWidget.setIconSize(QtCore.QSize(35, 35))
        # self.setBackPic(self,str(pathlib.Path(__file__).parent/'pic'/'backpic.bmp'))
        self.updategroup('''[["女神",["小龙女","周芷若","岳灵珊","小昭","仪琳"]],
                             ["黑名单",["小明","小红"]],
                             ["我的好友",["黄晔","朱安东","taoke"]],
                             ["速度",[]]]''')
        self.send_queue = send_queue
        self.rev_queue = rev_queue


    def searchicon(self, gpname2):
        if gpname2.find('好友') >= 0:
            return QtGui.QIcon(str(pathlib.Path(__file__).parent/'pic'/'buddy.ico'))
        elif gpname2.find('同事') >= 0:
            return QtGui.QIcon(str(pathlib.Path(__file__).parent/'pic'/'partner.ico'))
        elif gpname2.find('黑名单') >= 0:
            return QtGui.QIcon(str(pathlib.Path(__file__).parent/'pic'/'blacklist.ico'))
        else:
            return QtGui.QIcon(str(pathlib.Path(__file__).parent/'pic'/'buddy_default.ico'))

    def updategroup(self,jsonStr):
        self.friendTreeWidget.clear()
        self.friendTreeWidget.setStyleSheet("QTreeWidget{background-image: url(./ui/pic/backpic.bmp);color: black;}"
                                            "QTreeWidget::item{height:40px;width:40px;}"
                                            "QTreeWidget::item{margin:8px;}"
                                            "QTreeWidget::item:hover {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);border: 1px solid #bfcde4;}")

        self.groupdata = json.loads(jsonStr)

        for group in self.groupdata:
            g = QtWidgets.QTreeWidgetItem(self.friendTreeWidget)
            g.setText(0,group[0])
            g.setIcon(0,self.searchicon(group[0]))
            font = QtGui.QFont("yugothicyugothicuisemiboldyugothicuibold")
            font.setPointSize(14)
            g.setFont(0, font)
            for user in group[1]:
                u = QtWidgets.QTreeWidgetItem(g)
                u.setText(0,user)
                u.setIcon(0,self.get_zh_pic(user,True))
                font = QtGui.QFont('kaiti')
                font.setPointSize(16)
                u.setFont(0,font)
                u.setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.printallfriend()
        return self.friendTreeWidget

    @QtCore.pyqtSlot()
    def on_AddUserButton_clicked(self):
        d = adduserDlg(self)
        for g in self.groupdata:
            d.groupcomboBox.addItem(g[0])
        r = d.exec_()
        if r == 1:
            self.adduser(d.groupcomboBox.currentText(),d.usernamelineEdit.text())

    def printallfriend(self):
        print(self.groupdata)
        print('[',end='')
        for i in self.groupdata:
            print('[\'', end='')
            print(self.get_groupitem(i[0]).text(0),'\',[',end='')
            for j in i[1]:
                print('\'',end='')
                print(self.get_useritem(i[0],j).text(0),'\',',end='')
            print(']],', end='')
        print(']')

    def get_zh_pic(self,zh,state):
        font = pygame.font.SysFont('kaiti', 128)
        # 渲染图片，设置背景颜色和字体样式,前面的颜色是字体颜色
        ftext = font.render(zh[0], True, (65, 83, 130), (255, 255, 255) if state else (0,0,0))
        pygame.image.save(ftext, "zhpic.jpg")  # 图片保存地址
        return QtGui.QIcon("zhpic.jpg")

    def init_Ui(self):
        self.setWindowIcon(QtGui.QIcon(str(pathlib.Path(__file__).parent/'pic'/'logo.jpg')))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(str(pathlib.Path(__file__).parent/"pic/adduser.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AddUserButton.setIcon(icon1)
        # self.AddUserButton.clicked.connect(self.adduserButton_clicked)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(str(pathlib.Path(__file__).parent/"pic/weather.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.weatherButton.setIcon(icon2)
        self.weatherButton.clicked.connect(self.weatherButton_clicked)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(str(pathlib.Path(__file__).parent/"pic/calendar.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.calendarButton.setIcon(icon3)
        self.calendarButton.clicked.connect(self.calendarButton_clicked)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(str(pathlib.Path(__file__).parent/"pic/snack.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.snackButton.setIcon(icon4)
        self.snackButton.clicked.connect(self.snackButton_clicked)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(str(pathlib.Path(__file__).parent/"pic/Tetris.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.TetrisButton.setIcon(icon5)
        self.TetrisButton.clicked.connect(self.TetrisButton_clicked)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(str(pathlib.Path(__file__).parent/"pic/gobang.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.gobangButton.setIcon(icon6)
        self.gobangButton.clicked.connect(self.gobangButton_clicked)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(str(pathlib.Path(__file__).parent/"pic/file.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fileButton.setIcon(icon7)
        self.fileButton.clicked.connect(self.fileButton_clicked)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(str(pathlib.Path(__file__).parent/"pic/seting.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setingButton.setIcon(icon8)
        self.setingButton.clicked.connect(self.setingButton_clicked)
        # self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint) # 设置窗口总在最前
        self.friendTreeWidget.itemDoubleClicked.connect(self.friendTreeWidgetItemDoubleClicked)
    def weatherButton_clicked(self):
        print('weatherButton_clicked')

    def calendarButton_clicked(self):
        if MsgType.CALENDAR_DLG not in self.dlgstate:
            self.dlgstate.append(MsgType.CALENDAR_DLG)
            msg = MsgType(type=MsgType.MSG_FRIENDLIST,msgtype=MsgType.CALENDAR_DLG)
            self.send_queue.put(msg)

    def snackButton_clicked(self):
        pass

    def TetrisButton_clicked(self):
        if MsgType.TETRIS_DLG not in self.dlgstate:
            self.dlgstate.append(MsgType.TETRIS_DLG)
            msg = MsgType(type=MsgType.MSG_FRIENDLIST,msgtype=MsgType.TETRIS_DLG)
            self.send_queue.put(msg)

    def gobangButton_clicked(self):
        print('gobangButton_clicked')

    def fileButton_clicked(self):
        print('fileButton_clicked')

    def setingButton_clicked(self):
        print('setingButton_clicked')

    def deletegroup(self):
        s = self.friendTreeWidget.currentItem().text(0)
        gindex = self.searchgroup(s)
        reply = QtWidgets.QMessageBox.question(self, '警告', '确定要删除这个分组及其联系人吗？', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.friendTreeWidget.takeTopLevelItem(gindex)
            del self.groupdata[gindex]

    def creategroup(self,name):
        print('creategroup --> ',name)
        self.groupdata.append([name,[]])
        g = QtWidgets.QTreeWidgetItem(self.friendTreeWidget)
        g.setText(0, name)
        g.setIcon(0, self.searchicon(name))
        font = QtGui.QFont("yugothicyugothicuisemiboldyugothicuibold")
        font.setPointSize(14)
        g.setFont(0, font)

    def addgroup(self):
        gname, ok = QtWidgets.QInputDialog.getText(self, '提示信息', '请输入分组名称')
        if ok:
            if len(gname) == 0:
                QtWidgets.QMessageBox.information(self, '提示', '分组名称不能为空')
            else:
                self.creategroup(gname)

    def renamegroup(self):
        s = self.friendTreeWidget.currentItem().text(0)
        gnewname, ok = QtWidgets.QInputDialog.getText(self, '提示信息', '请输入分组的新名称')
        if ok:
            if gnewname == '':
                QtWidgets.QMessageBox.information(self, '提示', '分组名称不能为空哦')
            else:
                self.groupdata[self.searchgroup(s)][0] = gnewname
                self.friendTreeWidget.currentItem().setText(0, gnewname)
                newicon = self.searchicon(gnewname)
                self.friendTreeWidget.currentItem().setIcon(0, newicon)

    def searchgroup(self,item):
        for index,group in enumerate(self.groupdata):
            if item == group[0]:
                return index

    def deluser(self):
        self_text = self.friendTreeWidget.currentItem().text(0)
        parent_text = self.friendTreeWidget.currentItem().parent().text(0)
        uindex = self.searchuser(parent_text,self_text)
        self.friendTreeWidget.currentItem().parent().takeChild(uindex)
        del self.groupdata[self.searchgroup(parent_text)][1][uindex]

    def searchuser(self,groupname,user):
        for index,group in enumerate(self.groupdata[self.searchgroup(groupname)][1]):
            if user == group:
                return index

    def get_groupitem(self,group):
        item = self.friendTreeWidget.topLevelItem(0)
        try:
            while item.text(0) != group:
                item = self.friendTreeWidget.itemBelow(item)
        except:
            return None
        return item

    def get_useritem(self,group,user):
        p = self.get_groupitem(group)
        item = QtWidgets.QTreeWidgetItemIterator(p)
        try:
            while item.value().text(0) != user:
                item = item.__iadd__(1)
        except:
            return None
        return item.value()

    def adduser(self,groupname,user):
        for index,group in enumerate(self.groupdata):
            if groupname == group[0]:
                group[1].append(user)
                g = self.get_groupitem(groupname)
                u = QtWidgets.QTreeWidgetItem(g)
                u.setText(0,user)
                u.setIcon(0,self.get_zh_pic(user,True))
                font = QtGui.QFont('kaiti')
                font.setPointSize(16)
                u.setFont(0,font)
                u.setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)

    def moveuser(self):
        self_text = self.friendTreeWidget.currentItem().text(0)
        parent_text = self.friendTreeWidget.currentItem().parent().text(0)
        uindex = self.searchuser(parent_text,self_text)
        self.friendTreeWidget.currentItem().parent().takeChild(uindex)
        del self.groupdata[self.searchgroup(parent_text)][1][uindex]
        self.adduser(self.sender().text(),self_text)
        self.printallfriend()

    def contextMenuEvent(self, event):
        hititem = self.friendTreeWidget.currentItem()
        if hititem:
            root = hititem.parent()
            if root is None:
                pgroupmenu = QtWidgets.QMenu(self)
                pAddgroupAct = QtWidgets.QAction('添加分组',self.friendTreeWidget)
                pRenameAct = QtWidgets.QAction('重命名',self.friendTreeWidget)
                pDeleteAct = QtWidgets.QAction('删除该组',self.friendTreeWidget)
                pgroupmenu.addAction(pAddgroupAct)
                pgroupmenu.addAction(pRenameAct)
                pgroupmenu.addAction(pDeleteAct)
                pAddgroupAct.triggered.connect(self.addgroup)
                pRenameAct.triggered.connect(self.renamegroup)
                if self.friendTreeWidget.itemAbove(hititem) is None:
                    pDeleteAct.setEnabled(False)
                else:
                    pDeleteAct.triggered.connect(self.deletegroup)
                pgroupmenu.popup(self.mapToGlobal(event.pos()))
            else:
                usermenu = QtWidgets.QMenu(self)
                deluser = QtWidgets.QAction('删除联系人', usermenu)
                if len(self.groupdata) > 1:
                    moveuser = QtWidgets.QMenu('转移联系人至', usermenu)
                    usermenu.addMenu(moveuser)
                    for item in (i[0] for i in self.groupdata):
                        if item != root.text(0):
                            pMoveAct = QtWidgets.QAction(item, usermenu)
                            moveuser.addAction(pMoveAct)
                            pMoveAct.triggered.connect(self.moveuser)
                usermenu.addAction(deluser)
                deluser.triggered.connect(self.deluser)
                usermenu.exec_(QtGui.QCursor.pos())

    def closeEvent(self, QCloseEvent):
        msg_dict = MsgType(type=MsgType.MSG_FRIENDLIST,msgtype=MsgType.CLOSE_DLG)
        self.send_queue.put(msg_dict)
        QCloseEvent.ignore()

    @staticmethod
    def create_calendarDlg(queue):
        app = QtWidgets.QApplication(sys.argv)
        a = calendarDlg(send_queue = queue)
        app.exec_()

    def handle_rev_queue(self):
        if not self.rev_queue.empty():
            msg = self.rev_queue.get()
            print('dlg:',msg)
            if msg.type == MsgType.MSG_SYS:
                if msg.msgtype == MsgType.EXIT:
                    sys.exit(msg.msg)
                if msg.msgtype == MsgType.FRIENDLIST:
                    print(msg)

            if msg.type == MsgType.MSG_CALENDAR:
                if msg.msgtype == MsgType.CLOSE_DLG:
                    self.dlgstate.remove(MsgType.CALENDAR_DLG)

            if msg.type == MsgType.MSG_TETRIS:
                if msg.msgtype == MsgType.CLOSE_DLG:
                    self.dlgstate.remove(MsgType.TETRIS_DLG)

    def friendTreeWidgetItemDoubleClicked(self):
        hititem = self.friendTreeWidget.currentItem()
        if hititem.parent():
            print('friendTreeWidgetItemDoubleClicked:',self.friendTreeWidget.currentItem().text(0))


class adduserDlg(QtWidgets.QDialog,adduser.Ui_adduserDialog,basis.basis):
    '''添加好友对话框'''
    def __init__(self,parent = None):
        super(adduserDlg,self).__init__(parent)
        self.setupUi(self)
        self.init_Ui()

    def init_Ui(self):
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(str(pathlib.Path(__file__).parent/"pic/adduser.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.adduserButton.setIcon(icon1)
        self.adduserButton.clicked.connect(self.adduserButton_clicked)

    def adduserButton_clicked(self):
        if self.usernamelineEdit.text() == '':
            QtWidgets.QMessageBox.information(self, '提示', '好友名称不能为空哦')
        else:
            self.done(1)


class calendarDlg(QtWidgets.QWidget, _calendar.Ui_calendarDlg, basis.basis):
    '''日历对话框'''
    def __init__(self,send_queue,parent=None):
        self.send_queue = send_queue
        super(calendarDlg,self).__init__(parent)
        self.setupUi(self)
        path = pathlib.Path(__file__)
        self.setWindowIcon(QtGui.QIcon(str(path.parent / "pic" / "logo.jpg")))
        self.show()

    def closeEvent(self, QCloseEvent):
        msg = MsgType(type=MsgType.MSG_CALENDAR,msgtype=MsgType.CLOSE_DLG,msg = os.getpid())
        self.send_queue.put(msg)

class chatFrame(object):
    def __init__(self,name,time_ = time.localtime(),html = ''):
        self.name = name
        self.time = time_
        self.html = html
        self.path = self.get_zh_pic(self.name)

    def __repr__(self):
        html = '<div>' \
                    '<img src="%s" align="left" alt="" width="30" height="30">' \
                    '<b align="left">%s</b>' \
                '</div>' \
                    '<p>%s</p>' \
                    '<h6 align="center" style="color:blue">%s<\h6>' \
               '<br>'\
               %(self.path,self.name,self.html,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        return html

    def get_zh_pic(self,name):
        path = str(pathlib.Path(__file__).parent/('obj/%s.jpg'%self.name))
        font = pygame.font.SysFont('kaiti', 128)
        # 渲染图片，设置背景颜色和字体样式,前面的颜色是字体颜色
        ftext = font.render(name[0], True, (65, 83, 130), (255, 255, 255))
        pygame.image.save(ftext, path)  # 图片保存地址
        return path

class chatDlg(QtWidgets.QWidget, chat.Ui_chatDlg, basis.basis):
    CHAT_SETING_FILE = './chat_seting.pkl'
    def __init__(self,send_queue,username,targetname,parent = None):

        self.send_queue = send_queue
        self.username = username
        self.targetname = targetname
        self.tHtml = ''
        super(chatDlg, self).__init__(parent)
        self.setupUi(self)
        self.get_seting_from_file()
        self.init_Ui()
        self.show()

    def init_Ui(self):
        path = pathlib.Path(__file__)
        self.setWindowIcon(QtGui.QIcon(str(path.parent / "pic" / "logo.jpg")))
        self.setWindowTitle('微聊   %s'%self.username)
        self.SendButton.clicked.connect(self.sendButton_clicked)
        self.fontButton.clicked.connect(self.fontButtom_clicked)
        self.colorButton.clicked.connect(self.colorButtom_clicked)
        self.setBackPic(self, str(path.parent / "pic" / "chatback.bmp"))
        icon0 = QtGui.QIcon()
        icon0.addPixmap(QtGui.QPixmap(str(pathlib.Path(__file__).parent/"pic/font.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fontButton.setIcon(icon0)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(str(pathlib.Path(__file__).parent/"pic/colours.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.colorButton.setIcon(icon1)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(str(pathlib.Path(__file__).parent/"pic/send.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SendButton.setIcon(icon2)

    def sendButton_clicked(self):
        endstr = '</html>'
        editText = self.sendTextEdit.toPlainText()
        if editText == '':
            return
        html = str(self.textBrowser.toHtml())
        html = html[:-7]
        bs_sendEdit = bs4.BeautifulSoup(self.sendTextEdit.toHtml(),'html5lib')
        frame = chatFrame(self.username, html=str(bs_sendEdit.html.body))
        # bs_textBrowser = bs4.BeautifulSoup(self.textBrowser.toHtml(),'html5lib')
        html += str(frame)#str(bs_sendEdit.html.body)
        html += endstr
        print(html)
        self.textBrowser.setHtml(html)
        self.textBrowser.verticalScrollBar().setSliderPosition(self.textBrowser.verticalScrollBar().maximum())

    def setAllTextColor(self,color):
        sendstr = self.sendTextEdit.toPlainText()
        self.sendTextEdit.setTextColor(color)
        self.sendTextEdit.setText(self.sendTextEdit.toPlainText())
        cursor = self.sendTextEdit.textCursor()
        cursor.setPosition(len(sendstr))
        self.sendTextEdit.setTextCursor(cursor)

    def fontButtom_clicked(self):
        font, ok = QtWidgets.QFontDialog.getFont(QFont( self.seting['font_family'],
                                                        self.seting['font_pointSize'],
                                                        self.seting['font_weight'],
                                                        self.seting['font_italic']))
        if ok:
            self.sendTextEdit.setFont(font)
            self.seting['font_family'] = font.family()
            self.seting['font_weight'] = font.weight()
            self.seting['font_pointSize'] = font.pointSize()
            self.seting['font_italic'] = font.italic()
            self.save_seting_to_file()

    def colorButtom_clicked(self):
        col = QtWidgets.QColorDialog.getColor(self.seting['sendEdit_fontcolor'])
        if col.isValid():
            self.setAllTextColor(col)
            self.seting['sendEdit_fontcolor'] = col
            self.save_seting_to_file()

    def seting_sendedit_font_color(self):
        self.sendTextEdit.setFont(QFont(self.seting['font_family'],
                                        self.seting['font_pointSize'],
                                        self.seting['font_weight'],
                                        self.seting['font_italic']))
        self.setAllTextColor(QColor(self.seting['sendEdit_fontcolor']))

    def get_seting_from_file(self):
        try:
            file = open(self.CHAT_SETING_FILE,'rb')
            self.seting = pickle.load(file)
            self.seting_sendedit_font_color()
        except Exception as e:

            self.seting = {'font_family':'Arial',
                           'font_pointSize':9,
                           'font_weight':-1,
                           'font_italic':False,
                           'sendEdit_fontcolor':(0,0,0)}
            self.seting_sendedit_font_color()
            self.save_seting_to_file()

    def save_seting_to_file(self):
        with open(self.CHAT_SETING_FILE,'wb') as file:
            pickle.dump(self.seting,file)

if __name__ == "__main__":
    import sys
    pygame.init()
    q = Queue(10)
    app = QtWidgets.QApplication(sys.argv)
    a = chatDlg(q,'taoke','111')
    sys.exit(app.exec_())
















