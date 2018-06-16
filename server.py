from gevent import monkey, socket
import gevent
monkey.patch_all()
from socket import *
from multiprocessing import Process
import queue
from dataprocessing import *
import sys
from traceback import *
from random import *
from json import *
#from chatrobot import *
from wechatdatabase import WeChatDataBase
from time import *


class CoroutineServerBase(object):
    '''协程服务器'''

    def __init__(self, host=('0,0,0,0', 16888), debug=False):
        print('开始初始化')


        self.user = {}
        self.connected = []
        self.rcvdatapro = {}

        # 创建套接字
        self.sockfd = socket(AF_INET, SOCK_STREAM)
        # 设置套接字复用地址
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self.sockfd.bind(host)
        self.sockfd.listen(128)
        self.host = host


    @except_catcher
    def mainloop(self):
        
        print('进入接收')
        g1 = gevent.spawn(self.__accept, self.sockfd)
        g1.join()

        self.sockfd.close()


    def __accept(self, sockfd):

        while True:
            try:
                connfd, addr = sockfd.accept()
                print(connfd.getpeername(), '接入')
                gevent.spawn(self.__request, connfd)
            except Exception as e:
                print(e)
                print_exc()
                while True:
                    pass

    @except_catcher
    def __request(self, connfd):
        """处理客户端请求"""
        self.connected.append(connfd)
        self.rcvdatapro[connfd] = RcvDataProcessing()
        while True:
            data = connfd.recv(4096)
            if not data:
                break
            self.rcvdatapro[connfd].processing(data, lambda *args: self.recvfrom(connfd, *args))

        self.close(connfd)
    LOG_LEVEL = 2

    @except_catcher
    def output(self, level, *args):
        if level <= self.LOG_LEVEL:
            print(*args)

    def recvfrom(self, sockfd, source, target, time, dtype, data):
        pass

    @except_catcher
    def close(self, sockfd):
        del self.rcvdatapro[sockfd]
        self.connected.remove(sockfd)
        sockfd.close()


class Server(CoroutineServerBase):

    @except_catcher
    def __init__(self, host, debug=False):
        super().__init__(host, debug)
        self.database = WeChatDataBase()

    @except_catcher
    def sendto(self, sockfd, source, target, data, dtype='json', time=time()):
        packdata = DataProcessing.pack(source, target, dtype, data, time)
        #print('sendata:', packdata)
        sockfd.send(packdata)

    @except_catcher
    def senddata(self, user_name, source, target, data, dtype, time, need_cache=True):
        if user_name in self.user:
            self.sendto(self.user[user_name], source, target, data, dtype, time)
        elif bool(need_cache) is True:
            print(user_name, '不在线，消息写入缓存')
            self.write_cache(user_name, source, target, data, dtype, time)
        else:
            print('该消息不需要缓存')

    @except_catcher
    def sendto_user(self, source, target, data, dtype='json', time=time(), need_cache=True):
        if isinstance(target, str):
            target = UserID('user', target)

        self.senddata(target.name, source, target, data, dtype, time, need_cache)

    @except_catcher
    def sendto_group(self, source, target, data, dtype='json', time=time(), need_cache=True):
        if isinstance(target, str):
            target = UserID('group', target)

        for member in self.database.group_get_member(target.name):
            self.senddata(member, source, target, data, dtype, time, need_cache)
    
  
    @except_catcher
    def send_cache(self, user_name):
        caches = self.database.read_cache(user_name)
        for cache in caches:
            source, target, *args = loads(cache)
            source, target = UserID(source), UserID(target)
            # print(source, target, *args, sep='##')
            if target.dtype == 'user':
                self.sendto_user(UserID(source), UserID(target), *args)
            if target.dtype == 'group':
                self.sendto_group(UserID(source), UserID(target), *args)

    @except_catcher
    def write_cache(self, user_name, source, target, data, dtype, time):
        self.database.write_cache(user_name, dumps([str(source), str(target), data, dtype, time]))

    @except_catcher
    def close(self, connfd):
        # 判断socket是否是在线的用户的socket
        try:
            user_name, = [i for i in self.user if self.user[i] == connfd]
            self.go_offline(user_name)
            del self.user[user_name]
            self.output(1, user_name, '断开连接')
        except IndentationError as e:
            print(connfd, '断开连接')

        super().close(connfd)

    @except_catcher
    def go_online(self, user_name):
        ''' 上线 '''
        friendlist = self.database.get_friends(user_name)
        # print('好友列表：',friendlist)

        # 发送好友列表
        msg = dumps({'cmd': 'get_friends', 'args': {'args': None, 'result': friendlist}})
        self.sendto_user(UserID('server'), UserID('user', user_name), msg, need_cache=False)

        # 发送群组以及群成员
        groups = self.database.get_groups(user_name)
        grouplist = {group: self.database.group_get_member(group) for group in groups}

        msg = dumps({'cmd': 'group_and_members', 'args': {'args': None, 'result': grouplist}})
        self.sendto_user(UserID('server'), UserID('user', user_name), msg, need_cache=False)

        # 发送消息缓存
        self.send_cache(user_name)

        # 通知好友，我上线啦
        msg = dumps({'cmd': 'go_online', 'args': {'args': None, 'result': user_name}})
        for friend in friendlist:
            if friend in self.user:
                self.sendto_user(UserID('server'), UserID('user', friend), msg, need_cache=False)

    @except_catcher
    def go_offline(self, user_name):
        ''' 下线'''

        # 通知好友，我下线啦
        friendlist = self.database.get_friends(user_name)
        msg = dumps({'cmd': 'go_offline', 'args': {'args': None, 'result': user_name}})
        for friend in friendlist:
            if friend in self.user:
                self.sendto_user(UserID('server'), UserID('user', friend), msg, need_cache=False)

    @except_catcher
    def recvfrom(self, sockfd, source, target, time, dtype, recvdata):
        self.output(2, 'from ', sockfd.getpeername(), ' recv:',
                    source, target, time, dtype, recvdata)

        # 结果打包
        pack_result = lambda result: dumps({'cmd': data['cmd'], 'args': {'args': data['args'], 'result': result}})

        if target.dtype == 'server':
            data = Data.parse(dtype, recvdata)
            self.output(4, 'server data:', data)
            if source.dtype == 'server':
                # 自己发给自己的，就是关闭信号了
                print(sockfd.getpeername(), '断开连接')
                self.close(sockfd)

            elif data['cmd'] == 'get_online_user':
                regexp, start, stop = data['args']
                regexp = regexp if regexp != '' else '.*'
                reg = re.compile(regexp)
                matchs = [usr for usr in sorted(self.user) if reg.match(usr) is not None]
                self.sendto_user(UserID('server'), source, pack_result(matchs[start:stop:1]))

            elif data['cmd'] == 'is_online':
                usrlist = data['args']
                print(usrlist)
                reslist = [bool(usr in self.user) for usr in usrlist]
                self.sendto_user(UserID('server'), source, pack_result(reslist))

            elif data['cmd'] in self.database.interface():
                print('数据库处理')
                if data['cmd'] != 'sign_up' \
                        and data['cmd'] != 'sign_in' \
                        and source.name not in self.user:
                    print('未知连接:', sockfd, source)
                    return

                # 所有给数据库的就直接给了
                result = eval(
                    'self.database.{}(*{})'.format(data['cmd'], data['args']))

                #print('执行结果:', result)

                # 注册可以不通过名字发送
                if data['cmd'] == 'sign_up':
                    self.sendto(sockfd, UserID('server'), source, pack_result(result))

                # 登录的要记录一下,由于直接解析参数困难，干脆让数据库注册成功返回用户名了
                elif data['cmd'] == 'sign_in':
                    if result != False:
                        user_name = result
                        self.user[user_name] = sockfd
                        # 登录成功后，把好友列表，群组，离线信息全部下发
                        print('登录用户：', user_name)

                        # 发送登录结果
                        self.sendto_user(UserID('server'), user_name, pack_result(result))

                       # 上线的一些必要操作
                        self.go_online(user_name)
                    else:
                        # 登录失败的话，登录的用户名不一定存在，所以要直接通过socket返回
                        self.sendto(sockfd, UserID('server'), source, pack_result(result))

                # 发送，有些消息涉及到群发，所以发送函数统一不了
                elif data['cmd'] == 'group_drop' and result != False:
                    # 最后获取一下群成员，通知他们群被删除了
                    result, members = result

                    for member in members:
                        self.sendto_user(UserID('server'), member, pack_result(result))

                elif data['cmd'] in ['group_delete', 'group_create', 'group_append', 'group_transfer'] and result is not False:

                    self.sendto_group(UserID('server'), data['args'][0], pack_result(result))

                # 添加好友成功要给双方都发送消息,删除好友也一样
                elif data['cmd'] == 'make_friend' or data['cmd'] == 'delete_friend':
                    print('发送给双方消息')
                    userA, userB = result[1:]
                    self.sendto_user(UserID('server'), userA, pack_result(result))
                    self.sendto_user(UserID('server'), userB, pack_result(result))
                else:
                    self.sendto_user(UserID('server'), source, pack_result(result))
            else:
                print('%s 命令无法解析' % data['cmd'])
        # 发给用户的就直接转发
        elif target.dtype == 'user':
            self.output(4, 'userdata')
            self.sendto_user(source, target, recvdata, dtype)

        elif target.dtype == 'group':
            self.output(4, 'groupdata')
            self.sendto_group(source, target, recvdata, dtype)

        elif target.dtype == 'app':
            self.sendto(self, source, target, recvdata, dtype)
            
        else:
            print('未知类型：', type(target.dtype), target.dtype)

if __name__ == '__main__':
    server = Server(('0.0.0.0', 16888), debug=False)
    server.mainloop()
    # self.testprocess.join()