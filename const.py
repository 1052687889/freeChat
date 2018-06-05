#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
# Author:taoke

class MsgType(object):
    MSG_SYS = "MSG_SYS"               #系统消息 {'type':MSG_SYS,'msgtype':EXIT,'msg':0}
    MSG_LOGIN = "MSG_LOGIN"           #登陆消息
    MSG_REGISTER = "MSG_REGISTER"     #注册消息
    MSG_SOCKET = "MSG_SOCKET"
    MSG_FRIENDLIST = "MSG_FRIENDLIST"
    MSG_CALENDAR = "MSG_CALENDAR"
    MSG_SNACK = "MSG_SNACK"
    MSG_TETRIS = "MSG_TETRIS"

    EXIT = "EXIT"
    CLOSE_DLG = "CLOSE_DLG"
    FAILURE = "FAILURE"
    SUCCESS = "SUCCESS"
    CLOSE = "CLOSE"
    USER_DATA = "USER_DATA"
    FRIENDLIST = "FRIENDLIST"
    CALENDAR_DLG = "CALENDAR_DLG"
    SNACK_DLG = "SNACK_DLG"
    TETRIS_DLG = "TETRIS_DLG"
    def __init__(self,type,msgtype,msg=None):
        self.type = type
        self.msgtype = msgtype
        self.msg = msg

    def __repr__(self):
        return str({"type":self.type,"msgtype":self.msgtype,"msg":self.msg})



# if __name__ == "__main__":
#     a = MsgType()
#     print(a.create_msg('a','b'))
#







