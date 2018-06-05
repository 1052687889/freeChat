from socket import *
from dataprocessing import *
from time import *
from json import *
from queue import Queue


class Client(object):
    ''' 
        init(host,port)
        set_showevent(e)
        join(username)
        send(data)
    '''
    EVENT_CLOSE = 1

    def __init__(self, ip):
        self.ip = tuple(ip)
        self.sockfd = socket(AF_INET, SOCK_STREAM)
        self.sockfd.connect(self.ip)
        self.datapro = RcvDataProcessing()
        threading.Thread(target=self.rcv_thread).start()

    def recv_data(self, source, target, time, dtype, data):
        #print('recv is :', data)
        self.main(**data)

    def rcv_thread(self):
        while True:
            data = self.sockfd.recv(1024)
            if data == b'':
                break
            #print('recv:', data)
            self.datapro.processing(data, self.recv_data)
        
        #print('close')
        self.main(self.EVENT_CLOSE, '')

    def main(self, event, *args, **kwargs):
        pass

    def close(self):
        self.sockfd.close()

    def send(self, source, target, dtype, data):
        d = DataProcessing.pack(source, target, dtype, data)
        print('send[%d]:%s'%(len(d),d))
        self.sockfd.send(d)


class ClientAPI(Client):

    def __init__(self, ip):
        Client.__init__(self, ip)

        self.user = 'Anonymous'

    EVENT_LOGIN = 2
    EVENT_SUBMIT = 3
    EVENT_RECV = 4
    EVENT_MKFRIEND_REQUEST = 5  # 加好友请求
    EVENT_MKFRIEND_AGREED = 6
    EVENT_CHATDATA = 7
    EVENT_USER = 8
    EVENT_INPUT = 9
    EVENT_GETFRIEND = 10
    def api_main(self, event, *args, **kwargs):
        #print('main args:', args, kwargs)
        if event == self.EVENT_CLOSE:
            self.close()

        if event == self.EVENT_LOGIN:
            if args[0] == True:
                # 登录成功
                print('登录成功!')
            else:
                # 登录失败
                print('登录失败!')

        if event == self.EVENT_SUBMIT:
            if args[0] == True:
                # 注册成功
                print('注册成功!')

            else:
                # 注册失败
                print('注册失败!')

        if event == self.EVENT_RECV:
            # 解析数据
            pass

        if event == self.EVENT_MKFRIEND_AGREED:
            # 加好友成功，第一个参数为申请者，第二个参数为同意者
            friend = args[1] if self.user == args[0] else args[0]

            print('已经和%s成为好友了', friend)
            pass

        if event == self.EVENT_MKFRIEND_REQUEST:
            # 有人向你请求添加好友，参数为好友名
            print(args[0], '请求添加你为好友，是否同意 Y/N')
            self.response_friend(args[0], True if r == 'Y' else False)

            pass
        if event == self.EVENT_CHATDATA:
            # 聊天信息，
            source, time = args

            receiver = UserID.from_str(kwargs['receiver'])
            content = kwargs['content']
            if receiver.gettype() == 'user':
                # 发送给个人的
                print(time, source.getname(), ':\n', content)
        if event == self.EVENT_GETFRIEND:
            print('好友：',args)
    def recv_data(self, source, target, time, dtype, data):
        #print('recvdata:', source, target, time, dtype, data)
        data = Data.parse(dtype, data)
        if source.gettype() == 'server':
            if data['cmd'] == 'login':
                self.api_main(self.EVENT_LOGIN, data['args'])
            if data['cmd'] == 'submit':
                self.api_main(self.EVENT_SUBMIT, data['args'])
            if data['cmd'] == 'mkfriend':
                self.api_main(self.EVENT_MKFRIEND_AGREED, *data['args'])
            if data['cmd'] == 'getfriend':
                self.api_main(self.EVENT_GETFRIEND,*data['args'])
        if source.gettype() == 'user':
            if data['cmd'] == 'chatdata':
                self.api_main(self.EVENT_CHATDATA, source, time, **data['args'])
            if data['cmd'] == 'mkfriend':
                self.api_main(self.EVENT_MKFRIEND_REQUEST, source.getname())

    def sendto(self, target, dtype, data):
        self.send(UserID('user', self.user), target, dtype, data)

    def login(self, user, passwd):
        self.user = user
        data = {'cmd': 'login', 'args': {'user': user, 'passwd': passwd}}
        self.sendto(UserID('server'), 'json', dumps(data))

    def submit(self, user, passwd):
        data = {'cmd': 'submit', 'args': {'user': user, 'passwd': passwd}}
        self.sendto(UserID('server'), 'json', dumps(data))

    def send_data(self, target, content):
        data = {'cmd': 'chatdata', 'args': {
            'receiver': target.to_str(), 'content': content}}
        self.sendto(target, 'json', dumps(data))

    def request_friend(self, friend):
        '''请求添加好友
            friend:好友名
        '''
        data = {'cmd': 'mkfriend'}
        self.sendto(UserID('user', friend), 'json', dumps(data))

    def response_friend(self, friend, isaccept):
        '''添加好友响应'''
        data = {'cmd': 'mkfriend', 'args': {'userA': friend,
                                          'userB': self.user,
                                          'isaccept': isaccept}}
        self.sendto(UserID('server'), 'json', dumps(data))

    def get_friend(self):
        data = {'cmd': 'getfriend', 'args':self.user}
        self.sendto(UserID('server'), 'json', dumps(data))

    def group(self, operate, members):
        data = {'cmd': 'group', 'args': {
            'operate': operate, 'members': members}}
        self.send(UserID('server'), 'json', dumps(data))

    def create_group(self, members):
        self.group('create', members)

    def delete_group(self, group_name):
        self.group('delete', members)

    def group_append(self, members):
        self.group('append', members)




class Windows(ClientAPI):
    def __init__(self,ip):
        super().__init__(ip)
        self.queue = queue.Queue()
    def api_main(self, event, *args, **kwargs):
        #print('main args:', args, kwargs)
        if event == self.EVENT_CLOSE:
            self.close()

        if event == self.EVENT_LOGIN:
            if args[0] == True:
                # 登录成功
                print('登录成功!')
            else:
                # 登录失败
                print('登录失败!')

        if event == self.EVENT_SUBMIT:
            if args[0] == True:
                # 注册成功
                print('注册成功!')
            else:
                # 注册失败
                print('注册失败!')

        if event == self.EVENT_RECV:
            # 解析数据
            pass

        if event == self.EVENT_MKFRIEND_AGREED:
            # 加好友成功，第一个参数为申请者，第二个参数为同意者
            friend = args[1] if self.user == args[0] else args[0]

            print('已经和%s成为好友了'%friend)
            pass

        if event == self.EVENT_MKFRIEND_REQUEST:
            # 有人向你请求添加好友，参数为好友名
            print(args[0], '请求添加你为好友，是否同意 Y/N')
            self.queue.put(['mkfriend_request',args[0]])

        if event == self.EVENT_CHATDATA:
            # 聊天信息，
            source, time = args

            receiver = UserID.from_str(kwargs['receiver'])
            content = kwargs['content']
            if receiver.gettype() == 'user':
                # 发送给个人的
                print(time, source.getname(), ':\n', content)

        if event == self.EVENT_GETFRIEND:
            print('好友：',args)
        if event == self.EVENT_INPUT:
            cmd, *data = args[0].split()
            if cmd == 'response':
                if self.queue.empty():
                    pass
                else:
                    args = self.queue.get()
                    self.response_friend(args[1], True if data[0] == 'Y' else False)
            if cmd == 'submit':
                self.submit(*data,'123456')
            if cmd == 'login':
                self.login(*data,'123456')
            if cmd == 'sendto':
                self.send_data(UserID('user', data[0]), data[1])
            if cmd == 'mkfriend':
                self.request_friend(*data)
            if cmd == 'getfriend':
                self.get_friend()
    def _input(self):
        s = '发送格式:\n' + \
        '注册：submit 用户名　密码\n' + \
        '登录：login  用户名　密码\n' + \
        '发送: sendto 目标用户名　内容\n' + \
        '加好友: mkfriend 目标用户名\n' + \
        '>>>'
        self.api_main(self.EVENT_INPUT,input(s))



if __name__ == '__main__':

    # ip = ''
    # with open('ip.txt', 'r') as f:
    #     ip = loads(f.read())

    # print(ip)
    ip = ('119.28.82.227',16888)
    windows = Windows(ip)

    while True:
        windows._input()
    
    # clientgui = ClientGUI()
    # clientgui.set_sendevent(client.send)

    # clientgui.getted_username(client.join)
    # clientgui.mainloop()
