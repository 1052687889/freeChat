#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
# Author:taoke
from client import ClientAPI
from const import MsgType
class ClientNet(ClientAPI):
    def __init__(self,addr,send_queue):
        self.send_queue = send_queue
        super(ClientNet,self).__init__(addr)

    def api_main(self, event, *args, **kwargs):
        print('main args:', args, kwargs)
        if event == self.EVENT_CLOSE:
            print('socket close')
            msg = MsgType(type=MsgType.MSG_SOCKET,msgtype=MsgType.CLOSE)
            self.send_queue.put(msg)
            self.close()

        if event == self.EVENT_LOGIN:
            msg = MsgType(type=MsgType.MSG_LOGIN,msgtype = MsgType.SUCCESS if args[0] else MsgType.FAILURE)
            self.send_queue.put(msg)

        if event == self.EVENT_SUBMIT:
            msg = MsgType(type=MsgType.MSG_REGISTER,msgtype=MsgType.SUCCESS if args[0] else MsgType.FAILURE)
            self.send_queue.put(msg)

        if event == self.EVENT_GETFRIEND:
            msg = MsgType(type=MsgType.MSG_FRIENDLIST,msgtype=MsgType.FRIENDLIST,msg=args)
            self.send_queue.put(msg)




