#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
# Author:taoke
from queue import Queue
import threading,sys,time,multiprocessing
from PyQt5 import  QtWidgets
import pygame
from ui import myDlg
import netClient,tetris
from const import MsgType
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
        except IOError:
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
        d = myDlg.friendListDlg(application.rev_msg_queue,application.dlg_msg_queue)
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
                    sys.exit(msg.msg)

            elif msg.type == MsgType.MSG_LOGIN:
                if msg.msgtype == MsgType.CLOSE_DLG:
                    self.sys_exit()
                elif msg.msgtype == MsgType.USER_DATA:
                    try:
                        self.client.login(msg.msg['username'], msg.msg['passwd'])
                    except (IOError,AttributeError):
                        m = MsgType(type=MsgType.MSG_LOGIN,msgtype=MsgType.FAILURE)
                        self.dlg_msg_queue.put(m)
                        self.unconnect_server()
                    except Exception as e:
                        print(e)
                elif msg.msgtype == MsgType.SUCCESS:
                    application.dlg_msg_queue.put(msg)

            elif msg.type == MsgType.MSG_REGISTER:
                if msg.msgtype == MsgType.CLOSE_DLG:
                    self.sys_exit()
                elif msg.msgtype == MsgType.USER_DATA:
                    try:
                        self.client.submit(msg.msg['username'], msg.msg['passwd'])
                    except (IOError, AttributeError):
                        m = MsgType(type=MsgType.MSG_REGISTER,msgtype=MsgType.FAILURE)
                        self.dlg_msg_queue.put(m)
                        self.unconnect_server()
                    except Exception as e:
                        print(e)
                elif msg.msgtype == MsgType.SUCCESS:
                    application.dlg_msg_queue.put(msg)

            elif msg.type == MsgType.MSG_FRIENDLIST:
                if msg.msgtype == MsgType.CLOSE_DLG:
                    self.sys_exit()

                if msg.msgtype == MsgType.FRIENDLIST:
                    application.dlg_msg_queue.put(msg)

                if msg.msgtype == MsgType.CALENDAR_DLG:
                    queue = multiprocessing.Queue(3)
                    p = multiprocessing.Process(target=myDlg.friendListDlg.create_calendarDlg,args=(queue,))
                    p.daemon = True
                    p.start()
                    self.processingList.append([p,queue])

                if msg.msgtype == MsgType.SNACK_DLG:
                    pass

                if msg.msgtype == MsgType.TETRIS_DLG:
                    queue = multiprocessing.Queue(3)
                    p = multiprocessing.Process(target=tetris.run, args=(queue,))
                    p.daemon = True
                    p.start()
                    self.processingList.append([p, queue])

            if msg.type in [MsgType.MSG_CALENDAR,MsgType.MSG_SNACK,MsgType.MSG_TETRIS]:
                if msg.msgtype == MsgType.CLOSE_DLG:
                    application.dlg_msg_queue.put(msg)

            elif msg.type == MsgType.MSG_SOCKET:
                if msg.msgtype == MsgType.CLOSE:
                    self.unconnect_server()

                if msg.msgtype in [MsgType.FAILURE,MsgType.SUCCESS]:
                    application.dlg_msg_queue.put(msg)

        else:
            for i in self.processingList:
                if not i[1].empty():
                    msg = i[1].get()
                    if msg.type in [MsgType.MSG_CALENDAR,MsgType.MSG_SNACK,MsgType.MSG_TETRIS]:
                        if msg.msgtype == MsgType.CLOSE_DLG:
                            i[0].join()
                            self.processingList.remove(i)
                            m = MsgType(type=msg.type,msgtype=MsgType.CLOSE_DLG)
                            application.dlg_msg_queue.put(m)

    def join_all(self):
        for i in self.processingList:
            i.join()

    def clear_processing(self,target_pid):
        for i in self.processingList:
            if i[0].pid == target_pid:
                i[0].join()
                self.processingList.remove(i)

    def sys_exit(self):
        m = MsgType(type=MsgType.MSG_SYS, msgtype=MsgType.EXIT, msg=0)
        application.net_msg_queue.put(m)
        application.rev_msg_queue.put(m)
        application.dlg_msg_queue.put(m)

    def run(self):
        while True:
            self.handleMsg()


if __name__ == "__main__":
    app = application()
    app.run()



















