#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
# Author:taoke
from clientapi import *
from dataprocessing import *
from const import MsgType
import json
class ClientNet(ClientAPI):
    def __init__(self,addr,send_queue):
        self.send_queue = send_queue
        super(ClientNet,self).__init__(addr)

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

        if cmd == 'sign_up': # 注册结果
            msg = MsgType(type=MsgType.MSG_REGISTER,msgtype=MsgType.SUCCESS if recv_args else MsgType.FAILURE)
            self.send_queue.put(msg)

        if cmd == 'sign_in': # 登录结果
            if recv_args != False:
                self.user = recv_args
            msg = MsgType(type=MsgType.MSG_LOGIN, msgtype=MsgType.SUCCESS if recv_args else MsgType.FAILURE)
            self.send_queue.put(msg)

        if cmd == 'make_friend':
            # 如果拒绝则不会返回，这里返回Ｆａｌｓｅ的原因是：
            # １．两者中有一个不是用户
            # ２．双方已经是好友了
            result, userA, userB = recv_args  # Ａ为发起者
            msg = MsgType(type=MsgType.MSG_FRIENDLIST, msgtype=MsgType.ADDFRIEND,msg=['add_res',result,userA,userB])
            self.send_queue.put(msg)

        if cmd == 'delete_friend':
            # 如果失败则说明双方不是好友
            # Ａ删除Ｂ
            result, userA, userB = recv_args
            if self.user == userA:
                msg = MsgType(type=MsgType.MSG_FRIENDLIST, msgtype=MsgType.DELFRIEND,
                              msg=['del_res', result, userA, userB])
                self.send_queue.put(msg)
            else:
                msg = MsgType(type=MsgType.MSG_FRIENDLIST, msgtype=MsgType.DELFRIEND,
                              msg=['del_ret', result, userA, userB])
                self.send_queue.put(msg)

        if cmd == 'get_friends':
            data = []
            groupList = []
            self.is_online(recv_args)
            for i in recv_args:
                if recv_args[i] not in groupList:
                    groupList.append(recv_args[i])
                    data.append([recv_args[i],[i]])
                else:
                    for group in data:
                        if group[0] == recv_args[i]:
                            group[1].append(i)
            msg = MsgType(type=MsgType.MSG_FRIENDLIST,msgtype=MsgType.FRIENDLIST,msg=json.dumps(data))
            self.send_queue.put(msg)

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
            msg = MsgType(type=MsgType.MSG_FRIENDLIST, msgtype=MsgType.ONLINE, msg=zip(user_list,result_list))
            self.send_queue.put(msg)

        if cmd == 'go_online':
            # 好友上线通知
            msg = MsgType(type=MsgType.MSG_FRIENDLIST, msgtype=MsgType.ONLINE, msg=[(recv_args,True)])
            self.send_queue.put(msg)

        if cmd == 'go_offline':
            # 好友下线通知
            msg = MsgType(type=MsgType.MSG_FRIENDLIST, msgtype=MsgType.ONLINE, msg=[(recv_args,False)])
            self.send_queue.put(msg)

        if cmd == 'group_and_members':
            # 上线时，服务器主动下发组和组内成员
            #{'group1':m1,m2,..],'group2':[m1,m2,...]}
            group_list = recv_args
            print('群－成员表')
            # msg = MsgType(type=MsgType.MSG_REGISTER, msgtype=MsgType.SUCCESS if recv_args else MsgType.FAILURE)
            # self.send_queue.put(msg)
            for group in group_list:
                print("%s:\n\t%s" % (group, group_list[group]))

        if cmd == 'distribute_belong':
            user,friend,belong = send_args
            # result = recv_args
            # print('已变更%s为"%s"'%(friend,belong))
            msg = MsgType(type=MsgType.MSG_FRIENDLIST, msgtype=MsgType.ADDFRIEND,
                          msg=['change_belong_res', friend,belong,recv_args])
            self.send_queue.put(msg)


    def recvfrom_user(self, time, target, sender, cmd, recv_args, ):
        '''
            time  :    见recvfrom_server
            target:    见recvfrom_server
            sender：　  消息发送者的名字
            cmd   :    见recvfrom_server
            recv_args: 见recvfrom_server
        '''

        # print("sender:%s,cmd:%s,recv_args:%s" % (sender, cmd, recv_args))

        if cmd == 'chatdata':  # 聊天信息
            content = recv_args

            if target.dtype == 'user':  # 发送给个人的
                msg = MsgType(type=MsgType.MSG_FRIENDLIST,
                              msgtype=MsgType.CHAT_ORGIN_DATA,
                              msg=(sender, content))
                self.send_queue.put(msg)
            else:  # 群聊
                print(formattime(time), sender, '[%s]:\n' % target.name, content)

        if cmd == 'mkfriend':
            # 有人向你请求添加好友，参数为好友名
            # print(sender, '请求添加你为好友，是否同意 Y/N')
            # print('')
            # 同意，不同意则不理睬
            # self.make_friend(sender)
            msg = MsgType(type=MsgType.MSG_FRIENDLIST, msgtype=MsgType.ADDFRIEND, msg=['add_recv', sender])
            self.send_queue.put(msg)

