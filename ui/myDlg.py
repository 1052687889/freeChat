#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
# Author:taoke
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont,QColor
import sys,pathlib,json,os,time,pickle,queue,hashlib
import chat,basis,login,register,friendList,adduser,_calendar,friendapply
import pygame,bs4
from const import MsgType
from clientapi import *

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
        elif passwd != passwdsure:
            QtWidgets.QMessageBox.information(self.registerDlg, '提示', '两次密码不一致', QtWidgets.QMessageBox.Ok)
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
    def __init__(self, send_queue, rev_queue, username, parent=None):
        super(friendListDlg, self).__init__(parent)
        pygame.init()
        self.dlgstate = []
        self.username = username
        self.setupUi(self)
        self.init_Ui()
        self.friendTreeWidget.setIconSize(QtCore.QSize(35, 35))
        self.show()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.handle_rev_queue)
        self.timer.start(1)
        self.send_queue = send_queue
        self.rev_queue = rev_queue

    def init_Ui(self):
        self.setWindowTitle("微聊 - %s"%self.username)
        self.setWindowIcon(QtGui.QIcon(str(pathlib.Path(__file__).parent/'pic'/'logo.jpg')))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(str(pathlib.Path(__file__).parent/"pic/adduser.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AddUserButton.setIcon(icon1)
        self.AddUserButton.clicked.connect(self.adduserButton_clicked)
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
        icon6.addPixmap(QtGui.QPixmap(str(pathlib.Path(__file__).parent/"pic/robot.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.robotButton.setIcon(icon6)

        self.m_model = QtGui.QStandardItemModel(0, 1, self)
        m_completer = QtWidgets.QCompleter(self.m_model, self)
        self.findlineEdit.textChanged.connect(self.findlineEdit_textChanged)
        self.findlineEdit.setCompleter(m_completer)

        self.robotButton.clicked.connect(self.robotButton_clicked)

        self.friendTreeWidget.itemDoubleClicked.connect(self.friendTreeWidgetItemDoubleClicked)
        self.friendTreeWidget.clear()
        self.friendTreeWidget.setStyleSheet("QTreeWidget{background-image: url(./ui/pic/backpic.bmp);color: black;}"
                                            "QTreeWidget::item{height:40px;width:40px;}"
                                            "QTreeWidget::item{margin:8px;}"
                                            "QTreeWidget::item:hover {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);border: 1px solid #bfcde4;}")

    def searchicon(self, gpname2):
        if gpname2.find('好友') >= 0:
            return QtGui.QIcon(str(pathlib.Path(__file__).parent/'pic'/'buddy.ico'))
        elif gpname2.find('同事') >= 0:
            return QtGui.QIcon(str(pathlib.Path(__file__).parent/'pic'/'partner.ico'))
        elif gpname2.find('黑名单') >= 0:
            return QtGui.QIcon(str(pathlib.Path(__file__).parent/'pic'/'blacklist.ico'))
        else:
            return QtGui.QIcon(str(pathlib.Path(__file__).parent/'pic'/'buddy_default.ico'))

    def creategroup(self,name):
        g = QtWidgets.QTreeWidgetItem(self.friendTreeWidget)
        g.setText(0, name)
        g.setIcon(0, self.searchicon(name))
        font = QtGui.QFont("yugothicyugothicuisemiboldyugothicuibold")
        font.setPointSize(14)
        g.setFont(0, font)
        self.groupdata.append([name, [],g])

    def adduser(self,groupname,user,state=True):
        for index, group in enumerate(self.groupdata):
            if groupname == group[0]:
                u = QtWidgets.QTreeWidgetItem(group[2])
                u.setText(0, user)
                u.setIcon(0, self.get_zh_pic(user, state))
                font = QtGui.QFont('kaiti')
                font.setPointSize(16)
                u.setFont(0, font)
                u.setTextAlignment(0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                msgque = queue.Queue()
                group[1].append([user,u,state,msgque])

    def updategroup(self,jsonStr):
        data = json.loads(jsonStr)
        self.groupdata = []
        if data == []:
            self.creategroup('我的好友')
        else:
            for group in data:
                self.creategroup(group[0])
                for user in group[1]:
                    print(user)
                    self.adduser(group[0],user)
        self.printallfriend()
        return self.friendTreeWidget

    def printallfriend(self):
        for group in self.groupdata:
            print(group[0],[item[0] for item in group[1]],end='')
        print('')
        for group in self.groupdata:
            print(group[2].text(0),[item[1].text(0) for item in group[1]],end='')

    def findItem(self,username):
        for gindex,group in enumerate(self.groupdata):
            for uindex,user in enumerate(group[1]):
                if user[0] == username:
                    return gindex,uindex
        return None

    def adduserButton_clicked(self):
        self.d = adduserDlg(self)
        self.d.groupcomboBox.addItems((group[0] for group in self.groupdata))
        if self.d.exec_() == 1:
            if self.d.usernamelineEdit.text() == self.username:
                QtWidgets.QMessageBox.information(self, '提示', '不能添加自己为好友')
            else:
                if not self.findItem(self.d.usernamelineEdit.text()):
                    self.sendMsg( queue=self.send_queue,
                                  type_=MsgType.MSG_FRIENDLIST,
                                  msgtype_=MsgType.ADDFRIEND,
                                  msg_=['add',self.d.groupcomboBox.currentText(),self.d.usernamelineEdit.text()])
                    QtWidgets.QMessageBox.information(self, '提示', '已发送添加好友请求')
                else:
                    QtWidgets.QMessageBox.information(self, '提示', '%s已经是你的好友'%self.d.usernamelineEdit.text())

    def get_zh_pic(self,name,state):
        font = pygame.font.SysFont('kaiti', 128)
        # 渲染图片，设置背景颜色和字体样式,前面的颜色是字体颜色
        ftext = font.render(name[0], True, (65, 83, 130), (255, 255, 255) if state else (0,0,0))
        pygame.image.save(ftext, "zhpic.jpg")  # 图片保存地址
        return QtGui.QIcon("zhpic.jpg")

    def weatherButton_clicked(self):
        if MsgType.WEATHER_DLG not in self.dlgstate:
            self.dlgstate.append(MsgType.WEATHER_DLG)
            msg = MsgType(type=MsgType.MSG_FRIENDLIST,msgtype=MsgType.WEATHER_DLG)
            self.send_queue.put(msg)

    def calendarButton_clicked(self):
        if MsgType.CALENDAR_DLG not in self.dlgstate:
            self.dlgstate.append(MsgType.CALENDAR_DLG)
            msg = MsgType(type=MsgType.MSG_FRIENDLIST,msgtype=MsgType.CALENDAR_DLG)
            self.send_queue.put(msg)

    def snackButton_clicked(self):
        if MsgType.SNACK_DLG not in self.dlgstate:
            self.dlgstate.append(MsgType.SNACK_DLG)
            msg = MsgType(type=MsgType.MSG_FRIENDLIST,msgtype=MsgType.SNACK_DLG)
            self.send_queue.put(msg)

    def TetrisButton_clicked(self):
        if MsgType.TETRIS_DLG not in self.dlgstate:
            self.dlgstate.append(MsgType.TETRIS_DLG)
            msg = MsgType(type=MsgType.MSG_FRIENDLIST,msgtype=MsgType.TETRIS_DLG)
            self.send_queue.put(msg)


    def robotButton_clicked(self):
        print('robotButton_clicked')

    def deleteuser(self):
        self.sendMsg(queue = self.send_queue,
                     type_ = MsgType.MSG_FRIENDLIST,
                     msgtype_ = MsgType.DELFRIEND,
                     msg_ = ['del', self.friendTreeWidget.currentItem().text(0)])

    def delete_user_from_table(self,username):
        gIndex, uIndex = self.findItem(username)
        self.groupdata[gIndex][2].takeChild(uIndex)
        del self.groupdata[gIndex][1][uIndex]
        if len(self.groupdata[gIndex][1]) == 0:
            self.friendTreeWidget.takeTopLevelItem(gIndex)
            del self.groupdata[gIndex]
            if len(self.groupdata) == 0:
                self.creategroup('我的好友')

    def moveuser(self):
        self.sendMsg(queue = self.send_queue,
                     type_ = MsgType.MSG_FRIENDLIST,
                     msgtype_ = MsgType.MOVEFRIEND,
                     msg_ = ['move', self.friendTreeWidget.currentItem().text(0)])

    def findGroup(self,item):
        for index,group in enumerate(self.groupdata):
            if item == group[0]:
                return index
        return -1

    def contextMenuEvent(self, event):
        hititem = self.friendTreeWidget.currentItem()
        if hititem:
            root = hititem.parent()
            if root:
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
                deluser.triggered.connect(self.deleteuser)
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

    @staticmethod
    def createChatDlg(send_queue,rev_queue,username,targetname):
        app = QtWidgets.QApplication(sys.argv)
        a = chatDlg(send_queue=send_queue,rev_queue=rev_queue,username=username,targetname=targetname)
        app.exec_()

    def set_user_online_state(self,username,state):
        gIndex, uIndex = self.findItem(username)
        if self.groupdata[gIndex][1][uIndex][2] != state:
            self.groupdata[gIndex][1][uIndex][2] = state
            self.groupdata[gIndex][1][uIndex][1].setIcon(0, self.get_zh_pic(username,state))

    def handle_rev_queue(self):
        if not self.rev_queue.empty():
            msg = self.rev_queue.get()
            print('dlg:', msg)
            if msg.type == MsgType.MSG_SYS:
                if msg.msgtype == MsgType.EXIT:
                    sys.exit(msg.msg)

            if msg.type == MsgType.MSG_FRIENDLIST:
                if msg.msgtype == MsgType.FRIENDLIST:
                    self.updategroup(msg.msg)

                if msg.msgtype == MsgType.CHAT_ORGIN_DATA:
                    chatdlg_id = MsgType.CHAT_DLG + '_%s' % msg.msg[0]
                    gIndex, uIndex = self.findItem(msg.msg[0])
                    if chatdlg_id in self.dlgstate:
                        self.sendMsg(queue=self.send_queue,
                                     type_=MsgType.MSG_CHAT,
                                     msgtype_=MsgType.CHAT_DATA,
                                     msg_=msg.msg)
                    else:
                        self.groupdata[gIndex][1][uIndex][3].put(msg.msg)

                if msg.msgtype == MsgType.ADDFRIEND:

                    if msg.msg[0] == 'add_res':
                        if msg.msg[1] == False:
                            QtWidgets.QMessageBox.information(self, '提示', '添加好友{name} 失败'
                                                              .format(name=msg.msg[3] if msg.msg[2] == self.username else msg.msg[2]))
                        else:
                            # print('select group:',self.d.groupcomboBox.currentText())
                            self.sendMsg(queue=self.send_queue,
                                         type_=MsgType.MSG_FRIENDLIST,
                                         msgtype_=MsgType.ADDFRIEND,
                                         msg_=['change_belong',
                                               msg.msg[3] if msg.msg[2] == self.username else msg.msg[2],
                                               self.d.groupcomboBox.currentText()])

                    if msg.msg[0] == 'change_belong_res':
                        if msg.msg[3] == True:
                            if  self.findGroup(msg.msg[2]) == -1:
                                self.creategroup(msg.msg[2])
                            self.adduser(msg.msg[2],msg.msg[1])
                            gIndex = self.findGroup('我的好友')
                            if gIndex != -1:
                                if len(self.groupdata[gIndex][1]) == 0:
                                    self.friendTreeWidget.takeTopLevelItem(gIndex)
                                    del self.groupdata[gIndex]
                        else:
                            self.adduser('我的好友', msg.msg[1])

                    if msg.msg[0] == 'add_recv':
                        self.d = applyDlg([i[0] for i in self.groupdata],"%s申请加为好友"%msg.msg[1])
                        if self.d.exec_() == 1:
                            self.sendMsg(queue = self.send_queue,
                                         type_=MsgType.MSG_FRIENDLIST,
                                         msgtype_=MsgType.ADDFRIEND,
                                         msg_=['add_recv_ret',msg.msg[1]])

                if msg.msgtype == MsgType.DELFRIEND:
                    print('dlg:',msg)
                    if msg.msg[0] == 'del_res':
                        QtWidgets.QMessageBox.information(self, '提示', '删除好友{name} {res}'.format(name=msg.msg[3],res=fmt(msg.msg[1])))
                        if msg.msg[1] == True:
                            self.delete_user_from_table(msg.msg[3])

                    if msg.msg[0] == 'del_ret':
                        if msg.msg[1] == True:
                            QtWidgets.QMessageBox.information(self, '提示', '你被{name} 删除好友，节哀 >_<'.format(name=msg.msg[2]))
                            self.delete_user_from_table(msg.msg[2])

                if msg.msgtype == MsgType.ONLINE:
                    for item in msg.msg:
                        self.set_user_online_state(*item)

            if msg.type == MsgType.MSG_CALENDAR:
                if msg.msgtype == MsgType.CLOSE_DLG:
                    self.dlgstate.remove(MsgType.CALENDAR_DLG)

            if msg.type == MsgType.MSG_TETRIS:
                if msg.msgtype == MsgType.CLOSE_DLG:
                    self.dlgstate.remove(MsgType.TETRIS_DLG)

            if msg.type == MsgType.MSG_SNACK:
                if msg.msgtype == MsgType.CLOSE_DLG:
                    self.dlgstate.remove(MsgType.SNACK_DLG)
            if msg.type == MsgType.MSG_WEATHER:
                if msg.msgtype == MsgType.CLOSE_DLG:
                    self.dlgstate.remove(MsgType.WEATHER_DLG)
            if msg.type == MsgType.MSG_CHAT:
                if msg.msgtype == MsgType.CLOSE_DLG:
                    self.dlgstate.remove(MsgType.CHAT_DLG+'_%s'%msg.msg)

    def put_queue_msg_to_chatDlg(self,user):
        time.sleep(0.01)
        gIndex, uIndex = self.findItem(user)
        while not self.groupdata[gIndex][1][uIndex][3].empty():
            d = self.groupdata[gIndex][1][uIndex][3].get()
            print('threading',d)
            self.sendMsg(queue=self.send_queue,
                         type_=MsgType.MSG_CHAT,
                         msgtype_=MsgType.CHAT_DATA,
                         msg_= d)

    def findlineEdit_textChanged(self):
        text = self.findlineEdit.text()
        namelist = []
        userList = (user[0] for group in self.groupdata for user in group[1])
        for itm in userList:
            if itm.find(text) >= 0:
                if text == itm:
                    gIndex,uIndex = self.findItem(text)
                    self.groupdata[gIndex][2].setExpanded(True)
                    self.friendTreeWidget.setCurrentItem(self.groupdata[gIndex][1][uIndex][1])
                namelist.append(itm)
        self.m_model.removeRows(0, self.m_model.rowCount())
        for i in range(0, len(namelist)):
            self.m_model.insertRow(0)
            self.m_model.setData(self.m_model.index(0, 0), namelist[i])

    def friendTreeWidgetItemDoubleClicked(self):
        hititem = self.friendTreeWidget.currentItem()
        if hititem.parent():
            cur_user = self.friendTreeWidget.currentItem().text(0)
            chatdlg_id = MsgType.CHAT_DLG+'_%s'%cur_user
            if chatdlg_id not in self.dlgstate:
                self.dlgstate.append(chatdlg_id)
                self.sendMsg(queue=self.send_queue,
                             type_=MsgType.MSG_FRIENDLIST,
                             msgtype_=MsgType.CHAT_DLG,
                             msg_=(cur_user,))
                threading.Thread(target=self.put_queue_msg_to_chatDlg,args=(cur_user,)).start()

class adduserDlg(QtWidgets.QDialog,adduser.Ui_adduserDialog,basis.basis):
    '''添加好友对话框'''
    def __init__(self,parent = None):
        super(adduserDlg,self).__init__(parent)
        self.setupUi(self)
        self.init_Ui()

    def init_Ui(self):
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(str(pathlib.Path(__file__).parent/"pic/adduser.jpg")),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.adduserButton.setIcon(icon1)
        self.adduserButton.clicked.connect(self.adduserButton_clicked)

    def adduserButton_clicked(self):
        if self.usernamelineEdit.text() == '' or self.usernamelineEdit.text() == '':
            QtWidgets.QMessageBox.information(self, '提示', '组名或好友名称不能为空哦')
        else:
            self.done(1)

class applyDlg(QtWidgets.QDialog,friendapply.Ui_applyDialog,basis.basis):
    def __init__(self,grouplist,text,parent=None):
        self.groupList = grouplist
        super(applyDlg, self).__init__(parent)
        self.setupUi(self)
        self.init_Ui()
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.msglabel.setText(text)

    def init_Ui(self):
        self.agreeButton.clicked.connect(self.agreeButton_clicked)
        self.refuseButton.clicked.connect(self.refuseButton_clicked)
        for i in self.groupList:
            self.groupcomboBox.addItem(i)

    def agreeButton_clicked(self):
        self.done(1)

    def refuseButton_clicked(self):
        self.done(0)

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

import time
class chatFrame(object):
    def __init__(self,name,time_ = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),html = ''):
        self.name = name
        self.md5 = basis.basis.stringtomd5(self.name.encode())
        self.time = time_
        self.html = html
        self.path = str(pathlib.Path(__file__).parent/('obj/%s.jpg'%self.md5))
        self.get_zh_pic()

    def __repr__(self):
        html = '<div><img src="%s" align="left" alt="" width="30" height="30"><b align="left">%s</b></div><p>%s</p><h6 align="center" style="color:blue">%s<\h6><br>'\
               %(self.path,self.name,self.html,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        return html

    def getData(self):
        return self.html

    def get_zh_pic(self):
        try:
            file = open(self.path,'r')
            file.close()
        except:
            font = pygame.font.SysFont('kaiti', 128)
            # 渲染图片，设置背景颜色和字体样式,前面的颜色是字体颜色
            ftext = font.render(self.name[0], True, (65, 83, 130), (255, 255, 255))
            pygame.image.save(ftext, self.path)  # 图片保存地址

class chatDlg(QtWidgets.QWidget, chat.Ui_chatDlg, basis.basis):
    CHAT_SETING_FILE = './chat_seting.pkl'
    def __init__(self,send_queue,rev_queue,username,targetname,parent = None):
        pygame.init()
        self.send_queue = send_queue
        self.rev_queue = rev_queue
        self.username = username
        self.targetname = targetname
        self.tHtml = ''
        super(chatDlg, self).__init__(parent)
        self.setupUi(self)
        self.get_seting_from_file()
        self.init_Ui()
        self.show()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.handle_rev_queue)
        self.timer.start(20)


    def init_Ui(self):
        path = pathlib.Path(__file__)
        self.setWindowIcon(QtGui.QIcon(str(path.parent / "pic" / "logo.jpg")))
        self.setWindowTitle('微聊   %s -> %s'%(self.username,self.targetname))
        self.SendButton.clicked.connect(self.sendButton_clicked)
        self.fontButton.clicked.connect(self.fontButtom_clicked)
        self.colorButton.clicked.connect(self.colorButtom_clicked)
        self.sendTextEdit.currentCharFormatChanged.connect(self.sendEdit_currentCharFormatChanged)
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

    def sendEdit_currentCharFormatChanged(self):
        if self.sendTextEdit.toPlainText() == '':
            self.sendTextEdit.setTextColor(QColor(*self.allseting[self.username]['sendEdit_fontcolor']))

    def sendButton_clicked(self):
        endstr = '</html>'
        if self.sendTextEdit.toPlainText() == '':
            return
        html = str(self.textBrowser.toHtml())
        html = html[:-7]
        bs_sendEdit = bs4.BeautifulSoup(self.sendTextEdit.toHtml(),'html5lib')
        frame = chatFrame(self.username, html=str(bs_sendEdit.html.body))
        html += str(frame)
        self.sendMsg(queue=self.send_queue,
                     type_=MsgType.MSG_CHAT,
                     msgtype_=MsgType.CHAT_ORGIN_DATA,
                     msg_=(self.targetname,frame.getData()))
        html += endstr
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
        font, ok = QtWidgets.QFontDialog.getFont(self.getCurrentFont())
        if ok:
            self.allseting[self.username]['font_family'] = font.family()
            self.allseting[self.username]['font_weight'] = font.weight()
            self.allseting[self.username]['font_pointSize'] = font.pointSize()
            self.allseting[self.username]['font_italic'] = font.italic()
            self.save_seting_to_file()
            self.seting_sendedit_font_color()

    def colorButtom_clicked(self):
        col = QtWidgets.QColorDialog.getColor(QColor(*self.allseting[self.username]['sendEdit_fontcolor']))
        if col.isValid():
            self.allseting[self.username]['sendEdit_fontcolor'] = (col.red(), col.green(), col.blue())
            self.save_seting_to_file()
            self.seting_sendedit_font_color()

    def getCurrentFont(self):
        return QFont(self.allseting[self.username]['font_family'],
                     self.allseting[self.username]['font_pointSize'],
                     self.allseting[self.username]['font_weight'],
                     self.allseting[self.username]['font_italic'])

    def seting_sendedit_font_color(self):
        self.sendTextEdit.setFont(self.getCurrentFont())
        self.setAllTextColor(QColor(*self.allseting[self.username]['sendEdit_fontcolor']))

    def get_seting_from_file(self):
        defaultseting = {'font_family':'Arial',
                         'font_pointSize':12,
                         'font_weight':-1,
                         'font_italic':False,
                         'sendEdit_fontcolor':(0,0,0)}
        try:
            file = open(self.CHAT_SETING_FILE,'rb')
            self.allseting = pickle.load(file)
            try:
                self.seting_sendedit_font_color()
            except:
                self.allseting[self.username] = defaultseting
                self.seting_sendedit_font_color()
                self.save_seting_to_file()
        except Exception as e:
            self.allseting   = {self.username:defaultseting}
            self.seting_sendedit_font_color()
            self.save_seting_to_file()

    def save_seting_to_file(self):
        with open(self.CHAT_SETING_FILE,'wb') as file:
            pickle.dump(self.allseting,file)

    def closeEvent(self, QCloseEvent):
        msg = MsgType(type=MsgType.MSG_CHAT,msgtype=MsgType.CLOSE_DLG,msg = self.targetname)
        self.send_queue.put(msg)

    def handle_rev_queue(self):
        if not self.rev_queue.empty():
            msg = self.rev_queue.get()
            print('chatDlg:',msg)
            if msg.msgtype == MsgType.CHAT_DATA:
                endstr = '</html>'
                html = str(self.textBrowser.toHtml())
                html = html[:-7]
                frame = chatFrame(name=msg.msg[0], html=msg.msg[1])
                html += str(frame)
                html += endstr
                self.textBrowser.setHtml(html)
                self.textBrowser.verticalScrollBar().setSliderPosition(self.textBrowser.verticalScrollBar().maximum())




# if __name__ == "__main__":
#     # pygame.init()
#     # q = Queue(10)
#     # app = QtWidgets.QApplication(sys.argv)
#     # a = chatDlg(q,'taoke1','111')
#     # a.show()
#     # sys.exit(app.exec_())
#     # print('self.time:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#     # t = (2009, 2, 17, 17, 3, 38, 1, 48, 0)
#     # t = time.mktime(t)
#     # print(time.strftime("%b %d %Y %H:%M:%S", time.gmtime(t)))
#     # print(time.asctime(time.localtime(time.time())))
#     import time
#     print(time.strftime('%Y', time.localtime()))  # 获取完整年份
#
#











