#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
# Author:taoke
from queue import Queue
import hashlib
import threading,sys,time,multiprocessing
from PyQt5 import  QtWidgets
import pygame
from ui import myDlg
import netClient,tetris,snake_main
from const import MsgType
from dataprocessing import *
from Crawler import weatherApp

'''
起到转发消息到各个线程的作用
'''
class application(object):
    rev_msg_queue = Queue(50)      # 所有线程产生的消息发送至该队列
    dlg_msg_queue = Queue(50)      # 界面队列
    net_msg_queue = Queue(50)      # 网络消息队列
    processingList = []
    server_addr = ('119.28.82.227', 16888)

    def __init__(self):
        pygame.init()
        self.client = None
        threading.Thread(target=self.interface).start()
        threading.Thread(target=self.handle_other_event).start()

    def connect_server(self):
        try:
            msg = MsgType(type=MsgType.MSG_SOCKET, msgtype=MsgType.SUCCESS)
            self.client = netClient.ClientNet(application.server_addr, application.rev_msg_queue)
        except :
            msg.msgtype  = MsgType.FAILURE
            time.sleep(1)
        else:
            msg.msgtype = MsgType.SUCCESS
        finally:
            application.dlg_msg_queue.put(msg)

    def is_connect_server(self):
        return self.client != None

    def unconnect_server(self):
        self.client = None

    def interface(self):
        app = QtWidgets.QApplication(sys.argv)
        a = myDlg.registerLoginDlg(application.rev_msg_queue,application.dlg_msg_queue)
        app.exec_()
        del a,app
        app = QtWidgets.QApplication(sys.argv)
        d = myDlg.friendListDlg(application.rev_msg_queue,application.dlg_msg_queue,self.client.user)
        app.exec_()

    def handle_other_event(self):
        while True:
            if not self.is_connect_server():
                self.connect_server()

    def handleMsg(self):
        if not application.rev_msg_queue.empty():
            msg = application.rev_msg_queue.get()
            print('main:',msg)
            if msg.type == MsgType.MSG_SYS:
                if msg.msgtype == MsgType.EXIT:
                    self.join_all()
                    if self.client:
                        self.client.close()
                    sys.exit(msg.msg)

            elif msg.type == MsgType.MSG_LOGIN:
                if msg.msgtype == MsgType.CLOSE_DLG:
                    self.sys_exit()
                elif msg.msgtype == MsgType.USER_DATA:
                    try:
                        self.client.sign_in(msg.msg['username'], msg.msg['passwd'])
                    except (IOError,AttributeError):
                        m = MsgType(type=MsgType.MSG_LOGIN,msgtype=MsgType.FAILURE)
                        self.dlg_msg_queue.put(m)
                        self.unconnect_server()
                    except Exception as e:
                        print(e)
                elif msg.msgtype in [MsgType.SUCCESS,MsgType.FAILURE]:
                    application.dlg_msg_queue.put(msg)

            elif msg.type == MsgType.MSG_REGISTER:
                if msg.msgtype == MsgType.CLOSE_DLG:
                    self.sys_exit()
                elif msg.msgtype == MsgType.USER_DATA:
                    try:
                        self.client.sign_up(msg.msg['username'], msg.msg['passwd'])
                    except (IOError, AttributeError):
                        m = MsgType(type=MsgType.MSG_REGISTER,msgtype=MsgType.FAILURE)
                        self.dlg_msg_queue.put(m)
                        self.unconnect_server()
                    except Exception as e:
                        print(e)
                elif msg.msgtype in [MsgType.SUCCESS,MsgType.FAILURE]:
                    application.dlg_msg_queue.put(msg)

            elif msg.type == MsgType.MSG_FRIENDLIST:
                if msg.msgtype == MsgType.CLOSE_DLG:
                    # 好友列表对话框关闭消息
                    self.sys_exit()

                if msg.msgtype in [MsgType.FRIENDLIST,MsgType.ONLINE,MsgType.CHAT_ORGIN_DATA]:
                    # 转发从socke接收的好友列表消息
                    application.dlg_msg_queue.put(msg)

                if msg.msgtype == MsgType.ADDFRIEND:
                    # 加好友的消息
                    if msg.msg[0] == 'add':
                        # 发起添加好友
                        self.client.request_friend(msg.msg[2])

                    if msg.msg[0] in ['add_res','add_recv','change_belong_res']:
                        # 添加好友的结果和接受到好友申请
                        application.dlg_msg_queue.put(msg)
                    if msg.msg[0] == 'change_belong':
                        self.client.distribute_belong(msg.msg[1],msg.msg[2])

                    if msg.msg[0] in ['add_recv_ret']:
                        self.client.make_friend(msg.msg[1])

                if msg.msgtype == MsgType.DELFRIEND:
                    if msg.msg[0] == 'del':
                        self.client.delete_friend(msg.msg[1])

                    if msg.msg[0] in ['del_res','del_ret']:
                        application.dlg_msg_queue.put(msg)

                if msg.msgtype == MsgType.MOVEFRIEND:
                    if msg.msg[0] == 'move':
                        self.client.distribute_belong()
                if msg.msgtype == MsgType.CALENDAR_DLG:
                    self.createProcess(myDlg.friendListDlg.create_calendarDlg)

                if msg.msgtype == MsgType.SNACK_DLG:
                    self.createProcess(snake_main.main)

                if msg.msgtype == MsgType.WEATHER_DLG:
                    self.createProcess(weatherApp.main)

                if msg.msgtype == MsgType.CHAT_DLG:
                    s_queue = multiprocessing.Queue(3)
                    r_queue = multiprocessing.Queue(3)
                    chatdlg_id = MsgType.CHAT_DLG + '_%s' % msg.msg[0]
                    p = multiprocessing.Process(target=myDlg.friendListDlg.createChatDlg, args=(r_queue,s_queue,self.client.user,msg.msg[0],),name=chatdlg_id)
                    p.daemon = True
                    p.start()
                    self.processingList.append([p, r_queue,s_queue])

                if msg.msgtype == MsgType.TETRIS_DLG:
                    self.createProcess(tetris.run)

            if msg.type in [MsgType.MSG_CALENDAR,MsgType.MSG_SNACK,MsgType.MSG_TETRIS,MsgType.MSG_WEATHER]:
                if msg.msgtype == MsgType.CLOSE_DLG:
                    application.dlg_msg_queue.put(msg)

            elif msg.type == MsgType.MSG_SOCKET:
                if msg.msgtype == MsgType.CLOSE:
                    self.unconnect_server()

                if msg.msgtype in [MsgType.FAILURE,MsgType.SUCCESS]:
                    application.dlg_msg_queue.put(msg)

            elif msg.type == MsgType.MSG_CHAT:
                p = self.get_chat_processing(MsgType.CHAT_DLG + '_%s' % msg.msg[0])
                if p:
                    p[2].put(msg)
                else:
                    print('no find chat dlg:',msg)

        else:
            for i in self.processingList:
                if not i[1].empty():
                    msg = i[1].get()
                    if msg.type in [MsgType.MSG_CALENDAR,MsgType.MSG_WEATHER,MsgType.MSG_SNACK,MsgType.MSG_TETRIS,MsgType.MSG_CHAT]:
                        if msg.msgtype == MsgType.CLOSE_DLG:
                            i[0].join()
                            self.processingList.remove(i)
                            application.dlg_msg_queue.put(msg)

                        if msg.msgtype == MsgType.CHAT_ORGIN_DATA:
                            self.client.send_data(UserID('user', msg.msg[0]),msg.msg[1])

    def join_all(self):
        for i in self.processingList:
            i[0].join()

    def clear_processing(self,target_pid):
        for i in self.processingList:
            if i[0].pid == target_pid:
                i[0].join()
                self.processingList.remove(i)

    def get_chat_processing(self,processing_name):
        for i in self.processingList:
            if i[0].name == processing_name:
                return i

    def sys_exit(self):
        m = MsgType(type=MsgType.MSG_SYS, msgtype=MsgType.EXIT, msg=0)
        application.net_msg_queue.put(m)
        application.rev_msg_queue.put(m)
        application.dlg_msg_queue.put(m)

    def run(self):
        while True:
            self.handleMsg()

    def createProcess(self,func):
        queue = multiprocessing.Queue(1)
        p = multiprocessing.Process(target=func, args=(queue,))
        p.daemon = True
        p.start()
        self.processingList.append([p, queue])

if __name__ == "__main__":
    app = application()
    app.run()


















