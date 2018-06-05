# coding:utf8
from socket import *
import threading
import queue
import time
from dataprocessing import *
from select import *
import sys
from traceback import *
from random import *
from json import *
from database import *
from chatrobot import *

def save_ip(ip):
    with open('ip.txt','w') as f:
        f.write(dumps(ip))

class ServerBase(object):

    def __init__(self, ip):
        
        self.sockfd = socket(AF_INET, SOCK_STREAM)
        while True:
            try:
                port = 16888#randint(10000,65530)
                self.sockfd.bind((ip,port))
                break
            except OSError:
                pass
            else:
                save_ip((ip,port))
                break 
        self.serverip = tuple((ip,port))

        self.sockfd.listen()
        self.user = {}
        self.connected = []
        self.rcvdatapro = {}
        self.database = DataBase()

        threading.Thread(target = self.testThread).start()
        self.mainloop()

    LOG_LEVEL=3
    def output(self,level,*args):
        if level <= self.LOG_LEVEL:
            print(*args)
    #调试台
    def testThread(self):

        while True:
            try:
                a = input()

                if a == 'chatrobot':

                    self.robot = RobotClient(self.serverip)
                elif a == 'users':
                    print('在线人数:',len(self.user))
                elif a == 'friends':
                    b = input('请输入用户名')
                    if b == 'all':
                        for user in self.user:
                            print(user.ljust(8),':',*self.database.get_friends(user))
                    else:
                        print(b.ljust(8),':'*self.database.get_friends(b))
                elif 'loglevel' in a.lower():
                    s,l=split('=')
                    self.LOG_LEVEL = l
                elif a == 'connected' or a == 'c':
                    s = getattr(self,'connected')
                    print('connected:',[x.getpeername() for x in connected])
                elif a == 'user' or a == 'u':
                    print('user:',end = '')
                    for d in self.user:
                        print(d,self.user[d].getpeername())
                else:
                    print(a,': ',s)
            except NameError as ne:
                print(ne)
            except Exception:
                print_exc()


    def send(self, target, packdata):
        if isinstance(target, socket):
            targets = [target]
        try:
            for target in targets:
                self.output(2,'sendto:',target.getpeername(),packdata)
                target.send(packdata)
        except Exception as e:
            print('send error')
            print_exc()

    def mainloop(self):

        rlist = [self.sockfd]
        wlist = []
        xlist = []
        self.output(1,'服务器开始运行')
        while True:
            # print('connected:', [c.getpeername() for c in self.connected])
            rs, ws, xs = select(rlist+self.connected, wlist, xlist, 10)

            for r in rs:
                if r is self.sockfd:
                    connfd, addr = r.accept()
                    self.output(1,connfd.getpeername(), 'accept')
                    self.rcvdatapro[connfd] = RcvDataProcessing()
                    self.connected.append(connfd)

                else:
                    try:
                        # 解析数据
                        data = r.recv(1024)
                        #print('from',r.getpeername(),'recv:', data)
                        self.rcvdatapro[r].processing(
                            data, lambda source, target, time, dtype, data: self.main(r, source, target, time, dtype, data))
                        if data == b'':

                            self.close(r)

                    except Exception as e:
                        print('数据接收出错', e)
                        print_exc()
                        self.close(r)

            for w in ws:
                pass

            for x in xs:
                pass

    def main(self, connected, source, target, time, dtype, data):
        pass

    def close(self, connfd):
        connfd.close()
        del self.rcvdatapro[connfd]
        self.connected.remove(connfd)


class Server(ServerBase):

    def __init__(self, ip):
        ServerBase.__init__(self, ip)

    def recv(self):
        pass

    def sendto(self, connected, source, target, dtype, data):
        packdata = DataProcessing.pack(source, target, dtype, data)
        self.send(connected, packdata)

    def close(self,connfd):
        try:
            t = 0
            for i in self.user:
                if self.user[i] == connfd:
                    t = i
                    break
            del self.user[t]
            self.output(1,t,' 断开连接')
        except Exception as e:
            self.output(1,connfd.getpeername(),' 断开连接')
            pass
        super().close(connfd)

    def sendinfo(self,user):
        frinedinfo = self.database.getfriends(user)
        groupinfo = self.database.getgroups(user)
        appinfo = self.database.getapps(user)
        offlinecache = self.database.getofflinecache(user)


    def main(self, connected, source, target, time, dtype, recvdata):
        self.output(2,'from ', connected.getpeername(), ' recv:', source, target, time, dtype, recvdata)
        if target.gettype() == 'server':
            data = Data.parse(dtype, recvdata)
            self.output(4,'server data:',data)
            if source.gettype() == 'server':
                #自己发给自己的，就是关闭信号了
                print(connected.getpeername(), '断开连接')
                self.close(connected)

            if data['cmd'] == 'login':
                self.output(4,'login')
                ret = self.database.login(**data['args'])
                if ret is not False:
                    self.user[data['args']['user']] = connected
                result = dumps(
                    {'cmd': 'login', 'args': False if ret is False else True})
                self.sendto(connected,UserID('server'),source, 'json', result)

            if data['cmd'] == 'submit':
                self.output(4,'submit')
                ret = self.database.submit(**data['args'])
                result = dumps({'cmd': 'submit', 'args': ret})
                self.sendto(connected,UserID('server'),source, 'json', result)

            if data['cmd'] == 'mkfriend':
                self.output(4,'mkfriend')
                try:
                    #使用lambda保证字典解包后不会乱掉
                    f = lambda userA,userB,isaccept:(userA,userB,isaccept) 
                    userA, userB, isaccept = f(**data['args'])
                    if isaccept:
                        self.database.make_friend(userA, userB)
                        #source = UserID('server')
                        data = dumps({'cmd': 'mkfriend', 'args': (userA, userB)})
                        self.sendto(self.user[userA],UserID('server'),UserID('user',userA),'json',data)
                        self.sendto(self.user[userB],UserID('server'),UserID('user',userB),'json',data)
                except Exception as e:
                    print_exc()
            if data['cmd'] == 'getfriend':
                username = source.getname()
                print('username is',username)
                friend_list = self.database.get_friends(username)
                print('friend_list:',friend_list)
                data = dumps({'cmd':'getfriend','args':friend_list})
                self.sendto(self.user[username],UserID('server'),source,'json',data)


        if target.gettype() == 'user':
            self.output(4,'userdata')
            try:
                connfd = self.user[target.getname()]
                self.sendto(connfd, source, target, dtype, recvdata)
            except:
                #该用户不在线
                pass

        if target.gettype() == 'group':
            pass
            
            


            # if rdata['cmd'] == 'group':
            #     print('group')
            #     args = loads(rdata['args'])
            #     operate = args['operate']

            #     if operate == 'create':
            #         user = args['user']
            #         name = args['name']
            #         member = args['member']
            #         ret = self.database.create_group(user, name, member)
            #         data = dumps({'cmd': 'group', 'args': {
            #                      'operate': operate, 'name': name, 'result': ret}})
            #         self.sendto(dumps('server', ''), data)

            #     if operate == 'append':

            #         ret = self.database.group_append(user, name, member)
            #         rdata = dumps({'cmd': 'group', 'args': {
            #                       'operate': operate, 'name': name, 'result': ret}})
            #         self.sendto(dumps('server', ''), data)

            #     if operate == 'delete':
            #         user = args['user']
            #         name = args['name']
            #         member = args['member']


if __name__ == '__main__':
    try:
        server = Server('0.0.0.0')
        server.mainloop()
    except Exception as e:
        print('系统异常退出')
        print_exc()
        import sys
        sys.exit()
