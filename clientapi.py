# coding:utf-8
from socket import *
from dataprocessing import *
from time import *
from json import *
from queue import Queue


def fmt(result):
    if result is not False:
        return '成功'
    else:
        return '失败'


class Client(object):
    ''' 
        init(host,port)
        set_showevent(e)
        join(username)
        send(data)
    '''

    def __init__(self, ip):
        self.ip = tuple(ip)

        print('client init:', ip)
        self.sockfd = socket(AF_INET, SOCK_STREAM)
        self.sockfd.connect(self.ip)
        self.datapro = RcvDataProcessing()
        self.thread_runflag = True
        self.thread = threading.Thread(target=self.rcv_thread)
        self.thread.start()

    def recv_data(self, source, target, time, dtype, data):
        pass

    def rcv_thread(self):
        while self.thread_runflag:
            data = self.sockfd.recv(1024)
            if data == b'':
                break
            self.datapro.processing(data, self.recv_data)

        self.close()

    def main(self, event, *args, **kwargs):
        pass

    def close(self):
        self.thread_runflag = False
        self.sockfd.close()

    def send(self, source, target, dtype, data):
        d = DataProcessing.pack(source, target, dtype, data)
        #print('send[%d]:%s' % (len(d), d))
        self.sockfd.send(d)


class ClientAPI(Client):

    def __init__(self, ip):
        Client.__init__(self, ip)
        self.user = 'Anonymous'

    @except_catcher
    def close(self):
        super().close()
        self.testhtread_runflag = False

    @except_catcher
    def testhtread(self):
        while self.testhtread_runflag:
            cmd, *args = input().split()
            self.recv_data('input', cmd, args, None, None)

    @except_catcher
    def test(self, cmd, args, recv_args=None):
        print('cmd:%s,args:%s' % (cmd, args))
        if cmd == 'sign_up':
            print('sign_up', cmd, args)
            self.sign_up(args[0], '123456')

        if cmd == 'sign_in':
            self.sign_in(args[0], '123456')

        if cmd == 'sendto':
            self.send_data(UserID('user', args[0]), args[1])

        if cmd == 'mkfriend':
            self.request_friend(args[0])

        if cmd == 'delfriend':  # 删除好友

            self.delete_friend(args[0])

        if cmd == 'getfriend':  # 获取好友列表
            # 获取好友列表
            self.get_friends()

        if cmd == 'creategroup':  # 创建组
            # 成员列表最少要有两个变量，且第一个必须为创建者
            self.group_create('group_our', ['a', 'b', 'c', 'd'])

        if cmd == 'getgroup':
            self.get_groups()

        if cmd == 'getalluser':
            self.get_user()

        if cmd == 'getonline':
            self.get_online_user()

        if cmd == 'disbelong':
            self.distribute_belong('antony','维恩二')
    @except_catcher
    def recvfrom_server(self, time, target, cmd, send_args, recv_args):
        ''' 主要有些函数，比如查询某个组内成员，需要知道发送的什么参数。
            所以有个send_args的变量，不知道怎么用就打印出来看看就知道来了

            time:   为了时间同步问题，所以时间全部都是服务器上获取的（不然某一客户端改了本地时间就全乱了）
            　　　　　　  离线信息的时间为系统存储离线信息的时间

            target: 消息的目标位置，客户端收到的现在有两个属性 group 和　user　，如果为user则是发送给本人的
            　　　　　　　　如果为group，则需要判断是发给哪个群组的。

            cmd:    表明是哪个消息的返回
            send_args: 为了方便客户端处理，客户端发送的参数也一并被带下来了
            recv_args:　指令处理的结果

        '''
        print('time:%s,target:%s,cmd:%s,send:%s,recv:%s' % (formattime(time), target, cmd, send_args, recv_args))

        if cmd == 'sign_up':
            print('注册{}'.format(fmt(recv_args)))

        if cmd == 'sign_in':
            if recv_args != False:
                self.user = recv_args

            print('登录{}'.format(fmt(recv_args)))

        if cmd == 'make_friend':
            # 如果拒绝则不会返回，这里返回Ｆａｌｓｅ的原因是：
            # １．两者中有一个不是用户
            # ２．双方已经是好友了

            result, userA, userB = recv_args  # Ａ为发起者
            if self.user == userA:
                print('添加{}好友：{}'.format(userB, fmt(result)))
            else:
                print('{}添加你为好友：{}'.format(userA, fmt(result)))

        if cmd == 'delete_friend':
            # 如果失败则说明双方不是好友
            # Ａ删除Ｂ
            result, userA, userB = recv_args
            if self.user == userA:
                print('删除好友{}：{}'.format(userB, fmt(result)))
            else:
                if result:
                    print('你被%s删除了' % userA)
                else:
                    print('%s想删除你，但是失败了' % userA)

        if cmd == 'get_friends':
            #好友表

            friend_dict = recv_args

            maxlen = max(map(len,set(friend_dict)))
            for friend in friend_dict:
                print("{}/{}".format(friend.ljust(maxlen),friend_dict[friend]))

            self.is_online(friend_dict)

        if cmd == 'get_groups':
            group_list = recv_args
            print('群组列表:', group_list)

            for group in group_list:
                self.group_get_member(group)

        if cmd == 'group_create':
            # send_args:group_name,members
            # recv_args:True/False
            group_name, members = send_args
            result = recv_args

            print('创建组{}:{} {}'.format(group_name, members, fmt(recv_args)))

            # 测试获取组员
            # self.group_get_member(group_name)

            # 测试添加组员
            self.group_append(group_name, 'antony')
            # 测试发送组消息
            self.send_data(UserID('group', group_name), 'hello,everyone')

            # #测试删除组员
            # self.group_delete(group_name,'a')

            # #测试删除群
            # self.group_drop(group_name)

            # 测试群转让
            # self.group_transfer(group_name,'antony')
        if cmd == 'group_drop':
            group_name, user = send_args
            result = recv_args

            print('{}删除组{}:'.format(user, group_name, fmt(result)))

        if cmd == 'group_get_member':
            group_name = send_args[0]
            group_list = recv_args
            print('获取到了组员', group_name, group_list)

        if cmd == 'group_append':
            group_name, new_member = send_args
            result = recv_args
            print('群{}添加{}{}'.format(group_name, new_member, fmt(result)))

        if cmd == 'group_delete':
            group_name, admin, old_member = send_args
            result = recv_args
            print('群{},{}删除{}{}'.format(group_name, admin, old_member, fmt(result)))

        if cmd == 'group_transfer':
            group_name, old_admin, new_admin = send_args
            result = recv_args
            if result == True:
                print('{}成功把群{}转让给了{}'.format(old_admin, group_name, new_admin))
            else:
                print('{}想把群{}转让给{},但是失败了'.format(old_admin, group_name, new_admin))

        if cmd == 'get_user':
            regexp, start, stop = send_args
            result = recv_args

            if start == None:
                start = ''

            if stop == None:
                stop = ''

            print('所有用户："%s"[%s:%s:1]=%s' % (regexp, start, stop, result))

        if cmd == 'get_online_user':
            regexp, start, stop = send_args
            result = recv_args

            if start == None:
                start = ''

            if stop == None:
                stop = ''

            print('在线用户："%s"[%s:%s:1]=%s' % (regexp, start, stop, result))

        if cmd == 'is_online':
            user_list = send_args
            result_list = recv_args

            maxlen = max(map(len,user_list))
            for i in range(len(user_list)):
                print("%s:%s" % (user_list[i].ljust(maxlen), '在线' if result_list[i] else '不在线'))

        if cmd == 'go_online':
            # 好友上线通知
            # send_args is None
            friend = recv_args
            print('好友%s上线啦' % friend)

        if cmd == 'go_offline':
            # 好友下线通知
            # send_args is None
            friend = recv_args
            print('好友%s下线啦' % friend)

        if cmd == 'group_and_members':
            # 上线时，服务器主动下发组和组内成员
            #{'group1':m1,m2,..],'group2':[m1,m2,...]}
            group_list = recv_args
            print('群－成员表')
            for group in group_list:
                print("%s:\n\t%s" % (group, group_list[group]))

        if cmd == 'distribute_belong':
            user,friend,belong = send_args
            result = recv_args

            print('已变更%s为"%s"'%(friend,belong))

    @except_catcher
    def recvfrom_user(self, time, target, sender, cmd, recv_args,):
        '''
            time  :    见recvfrom_server
            target:    见recvfrom_server
            sender：　  消息发送者的名字
            cmd   :    见recvfrom_server
            recv_args: 见recvfrom_server
        '''

        print("sender:%s,cmd:%s,recv_args:%s" % (sender, cmd, recv_args))

        if cmd == 'chatdata':  # 聊天信息
            content = recv_args

            if target.dtype == 'user':  # 发送给个人的
                print(formattime(time), sender, ':\n', content)
            else:  # 群聊
                print(formattime(time), sender, '[%s]:\n' % target.name, content)

        if cmd == 'mkfriend':
            # 有人向你请求添加好友，参数为好友名
            print(sender, '请求添加你为好友，是否同意 Y/N')

            # 同意，不同意则不理睬
            self.make_friend(sender)

    @except_catcher
    def recv_data(self, source, target, time, dtype, data):
        #print('recvdata:', source, target, time, dtype, data)

        if source == 'input':  # 调试接口

            self.test(target, time)
            return

        data = Data.parse(dtype, data)
        if source.dtype == 'server':
            self.recvfrom_server(time, target, data['cmd'],
                                 data['args']['args'], data['args']['result'])
        if source.dtype == 'user':
            self.recvfrom_user(time, target, source.name, data['cmd'], data['args'])

    @except_catcher
    def sendto(self, target, data, dtype='json'):
        self.send(UserID('user', self.user), target, dtype, data)

    @except_catcher
    def send_data(self, target, content):

        data = {'cmd': 'chatdata', 'args': content}

        self.sendto(target, dumps(data))


    def request_friend(self, friend):
        '''请求添加好友
            friend:好友名
        '''
        data = {'cmd': 'mkfriend', 'args': None}
        self.sendto(UserID('user', friend), dumps(data))

    def sendto_server(self, cmd, *args):
        data = {'cmd': cmd, 'args': args}
        self.sendto(UserID('server'), dumps(data))

    def sign_up(self, user, passwd):
        '''注册'''
        self.sendto_server('sign_up', user, passwd)

    def sign_in(self, user, passwd):
        '''登录'''
        self.sendto_server('sign_in', user, passwd)

    def make_friend(self, friend):
        '''加好友'''
        self.sendto_server('make_friend', friend, self.user)

    def delete_friend(self, friend):
        self.sendto_server('delete_friend', self.user, friend)

    def get_friends(self):
        self.sendto_server('get_friends', self.user)

    def get_groups(self):
        self.sendto_server('get_groups', self.user)

    def group_create(self, group_name, members):
        # 保证组名唯一性
        group_name = group_name + '_' + self.user + str(int(time()))

        self.sendto_server('group_create', group_name, [self.user] + members)

    def group_drop(self, group_name):
        '''这里的组名必须是那个唯一的'''
        self.sendto_server('group_drop', group_name, self.user)

    def group_get_member(self, group_name):
        self.sendto_server('group_get_member', group_name)

    def get_group_owner(self, group_name):
        ''' 获取群主
            这个函数估计用不到，获取的组员列表第一个参数就是群主
        '''
        self.sendto_server('get_group_owner', group_name)

    def group_append(self, group_name, user):
        '''　往群组内添加成员 '''

        self.sendto_server('group_append', group_name, user)

    def group_delete(self, group_name, member):
        ''' 删除组员
            只有本人或者群主才能删除
        '''
        self.sendto_server('group_delete', group_name, self.user, member)

    def group_transfer(self, group_name, user):
        ''' 转让群主 
            只有群主才有权限
        '''
        self.sendto_server('group_transfer', group_name, self.user, user)

    def get_user(self, regexp='', start=None, stop=None):
        ''' 获取所有用户名,采用正则匹配，但如果输入为空的话会匹配所有的人
            count 为 获取范围　返回结果为 result[count[0]:count[1]:1]
        '''
        self.sendto_server('get_user', regexp, start, stop)

    def get_online_user(self, regexp='', start=None, stop=None):
        '''获取在线人数'''
        self.sendto_server('get_online_user', regexp, start, stop)

    def is_online(self, user_list):
        ''' 查询用户是否在线
            输入必须为列表
        '''
        self.sendto_server('is_online', *user_list)

    def distribute_belong(self,friend,belong):
        '''变更好友分组'''
        self.sendto_server('distribute_belong',self.user,friend,belong)

if __name__ == '__main__':

    
    s = '发送格式:\n' + \
        '注册：sign_up 用户名　密码\n' + \
        '登录：sign_in  用户名　密码\n' + \
        '发送: sendto 目标用户名　内容\n' + \
        '>>>'

    # '加好友: mkfriend 目标用户名\n' + \
    # '创建组: create 组名　成员\n' + \
    # '添加成员: append 组名　成员\n' + \
    # '删除组：drop 组名\n' + \
    # '删除组员：delete 组名 成员\n' + \
    # '更新组信息：update\n' + \
    

    ip = ('119.28.82.227',16888)
    #ip = ('localhost',16888)
    print(s)
    client = ClientAPI(ip)
    try:
        while True:
            pass

    except:
        client.close()

