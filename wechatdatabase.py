# coding:utf-8
from databaseinterface import DataBaseInterface
import re

#日志输出接口
def debug_print(*args,**kwargs):
    #print(*args,**kwargs)
    pass

class WeChatDataBase(DataBaseInterface):
    '''
        bool sign_up(user,passwd) 注册
        bool sign_in(user,passwd) 登录
        bool is_user(user) 判断user是否注册过
        bool is_friend(userA,userB) 判断userA 和 userB是否为好友
        bool make_friend(userA,userB) 使userA 和 userB成为好友
        dict get_friends(user) 获取user的所有好友
        bool delete_friend(userA,userB) 断绝userA 和　userB的好友关系
        bool distribute_belong(user,friend,belong)  ,更变好友属组
        list get_groups(user)  获取user的所有组信息
        bool group_create(group_name,members) member 第一个人为群主
        list group_get_member(group_name) 获取所有群成员 
        str  group_get_onwer(group_name)  获取群主
        bool group_is_exist(group_name,user) 判断user是否在群组内  
        bool group_drop(group_name,user) 删除群组,user必须为群主
        bool group_append(group_name,user) 把user添加入群
        bool group_delete(group_name,user,member) 删除群中的member,user必须为群主或者member本人
        bool group_transfer(group_name,userA,userB) 把群转让给userB,userA必须为群主
        bool write_cache(user,cache(str)) 写入user的缓存消息
        list read_cache(user,cache(str)) 　读取user的缓存消息

        list get_user(self,where='',start=None,stop=None): 用正则表达式获取所有的用户
    '''

    def __init__(self):
        super().__init__('root', '123456')

        if not self.is_exist('wechat'):
            self.create('wechat')

    def interface(self):
        return ['sign_up','sign_in','is_user','get_user',
        'is_friend','make_friend','get_friends','delete_friend',
        'get_groups','group_create','group_get_member','distribute_belong',
        'group_get_onwer','group_is_exist','group_drop','group_append',
        'group_delete','group_transfer','write_cache','read_cache']

    def _userfriend(self, user):
        return 'wechat.' + user + 'friends'

    def _grouptable(self, group):
        return 'wechat.' + group + 'group'

    def _usergroup(self,user):
        return 'wechat.' + user+'groups'

    def _usercache(self, user):
        return 'wechat.'+user+'offlinecache'

    def sign_up(self, user, passwd):

        if not self.is_exist('wechat.user'):
            self.create('wechat.user', ('name char(20)', 'password char(20)'))

        if self.select('wechat.user', where="name = '{}'".format(user)):
            debug_print('该用户已存在')
            return False
        else:
            debug_print('创建新用户:{}'.format(user, passwd))
            self.insert('wechat.user', (user, passwd)).commit()
            return True

    def sign_in(self, user, passwd):
        if not self.is_exist('wechat.user'):
            return False
        try:
            ret = self.select('wechat.user', field='password',
                              where="name = '{}'".format(user))
            if ret[0][0] == passwd:
                return user
            else:
                return False
        except Exception:
            return False

    def get_user(self,where='',start=None,stop=None):
        try:
            if not self.is_exist('wechat.user'):
                return []
            else:
                where = where if where != '' else '.*'
                ret = self.select('wechat.user',field = 'name',where = "name regexp '{}'".format(where))
                return [x[0] for x in ret][start:stop:1]
        except:
            return []

    def is_user(self,user):
        if self.select('wechat.user',where="name = '{}'".format(user)):
            return True
        else:
            return False

    def is_friend(self, userA, userB):

        userA_friend_table = self._userfriend(userA)
        userB_friend_table = self._userfriend(userB)

        if not self.is_exist(userA_friend_table):
            return False

        if not self.is_exist(userB_friend_table):
            return False

        if not self.select(userA_friend_table, field = 'friends', where='friends = "%s"' % userB):
            return False 

        if not self.select(userB_friend_table, field = 'friends', where='friends = "%s"' % userA):
            return False

        return True

    #分配属组
    def distribute_belong(self,user,friend,belong):

        if not self.is_friend(user, friend):
            return False

        user_friend_table = self._userfriend(user)

        belong = 'belong="{}"'.format(belong)
        where = 'friends="{}"'.format(friend)

        self.update(user_friend_table,(belong,),where).commit()
        return True

    def make_friend(self, userA, userB):

        if not self.is_user(userA) or not self.is_user(userB):
            debug_print('%s或%s不是用户,加好友失败'%(userA,userB))
            return False,userA, userB

        if self.is_friend(userA, userB):
            debug_print('%s或%s已经是好友了,加好友失败'%(userA,userB))
            return False,userA, userB

        userA_friend_table = self._userfriend(userA)
        userB_friend_table = self._userfriend(userB)

        self.create_if_not_exist(userA_friend_table, ('friends char(20)','belong char(20)'))
        self.create_if_not_exist(userB_friend_table, ('friends char(20)','belong char(20)'))

        self.insert(userA_friend_table, (userB,'我的好友')).commit()
        self.insert(userB_friend_table, (userA,'我的好友')).commit()
        return True,userA, userB

    def delete_friend(self, userA, userB):
        if not self.is_friend(userA, userB):
            return False,userA, userB

        userA_friend_table = self._userfriend(userA)
        userB_friend_table = self._userfriend(userB)

        self.delete(userA_friend_table,
                    where='friends = "{}"'.format(userB)).commit()
        self.delete(userB_friend_table,
                    where='friends = "{}"'.format(userA)).commit()
        return True,userA, userB

    def get_friends(self, user):
        user_friend_table = self._userfriend(user)

        if not self.is_exist(user_friend_table):
            return {}

        return {x[0]:x[1] for x in self.select(user_friend_table)}
    def get_groups(self,user):
        user_groupstable = self._usergroup(user)

        if not self.is_exist(user_groupstable):
            return []
        return [x[0] for x in self.select(user_groupstable)]

    def group_create(self, group, members):
        group_table = self._grouptable(group)

        for member in members:
            if not self.is_user(member):
                debug_print('%s不是用户'%member)
                return False

        if self.is_exist(group_table):
            debug_print('组名已存在')
            return False

        self.create_if_not_exist(
            group_table, ('id int', 'member char(20)'),
            primary='id', auto_increment=1)

        creator_table = self._usergroup(members[0])
        self.create_if_not_exist(creator_table,'groups char(80)')

        self.insert(creator_table,(group,)).commit()


        for member in members:
            self.insert(group_table, (None, member))

        self.commit()
        debug_print('创建成功')
        return True


    def group_drop(self, group, user):
        group_name = self._grouptable(group)
        user_groupstable = self._usergroup(user)    

        
        if user != self.get_group_owner(group):
            return False

        debug_print(group_name)

        members = self.group_get_member(group)

        self.drop(group_name)

            
        self.delete(user_groupstable,where='groups="{}"'.format(group))
        return True,members


    def group_get_member(self, group):

        group_table = self._grouptable(group)

        if not self.is_exist(group_table):
            return []

        return [x[0] for x in self.select(group_table, field='member')]

    def get_group_owner(self, group):
        group_table = self._grouptable(group)

        if not self.is_exist(group_table):
            return None

        ret = self.select(group_table, field='member', where='id=1')

        #兼容了返回值是None的情况
        return (ret or [(None,)])[0][0]


    def group_is_exist(self, group, user):
        '''判断某个成员是否在组内'''
        group_table = self._grouptable(group)
        if not self.is_exist(group_table):
            return False

        if self.select(group_table, field='member', where='member="%s"' % user):
            return True

        else:
            return False

    def group_append(self, group, user):

        if not self.is_user(user):
            return False

        group_table = self._grouptable(group)

        if self.group_is_exist(group,user):
            return False
        else:
            self.insert(group_table, (None, user)).commit()
            return True

    def group_delete(self, group, user, member):
        group_table = self._grouptable(group)

        group_owner = self.get_group_owner(group)

        if group_owner != user and member != user:
            # 只有群主或者本人有权限删除成员
            return False

        if group_owner == user and user == member:
            # 群主删除自己

            return False

        if not self.group_is_exist(group, member):
            # 要删除的人不在群里
            return False

        self.delete(group_table, where='member = "%s"' % member).commit()
        return True

    def group_transfer(self, group, userA, userB):
        '''userA 转让 给 userB'''
        group_table = self._grouptable(group)

        if self.get_group_owner(group) != userA:
            # 非群主无转让权限
            return 'No Permission'

        if not self.group_is_exist(group, userB):
            # Ｂ不在群里
            return 'Not a Member'

        # 获取成员列表
        members = self.group_get_member(group)
        # 删除组
        self.group_drop(group,userA)
        # 新建组
        members.remove(userB)
        self.group_create(group, [userB] + members)
        return True

    def write_cache(self, user, cache):
        offline_table = self._usercache(user)

        self.create_if_not_exist(
            offline_table,'content varchar(21800)')

        if isinstance(cache, str):
            cache = [cache]

        for c in cache:
            self.insert(offline_table, (c,))
        self.commit()

    def read_cache(self, user):
        offline_table = self._usercache(user)

        if not self.is_exist(offline_table):
            return []

        ret = [x[0] for x in self.select(offline_table)]
        self.drop(offline_table)
        return ret

        # 按顺序输出

#create table abcd(group char(10));
import time
if __name__ == '__main__':
    db = WeChatDataBase()
    # debug_print('sign_up:',db.sign_up('yalisa','123456'))
    # debug_print('sign_up:',db.sign_up('antony','123456'))
    # debug_print('sign_up:',db.sign_up('lily','123456'))
    # debug_print('sign_up:',db.sign_up('silika','123456'))
    # debug_print('sign_up:',db.sign_up('anny','123456'))
    user_list = ['yalisa','antony','lily','silika','anny','a','b','c','d','e']
    # for user in user_list:
    #     db.sign_up(user,'123456')

    # for user in user_list[1:]:
    #     db.make_friend('yalisa',user)

    db.distribute_belong('yalisa','anny','挚友')
    print(db.get_friends('yalisa'))
    #print('regexp:',db.get_user(''))

    # print(db.select('wechat.user'))
    # group_name = 'asfdnaofha'

    # #et = db.create('wechat.abcd1','groups char(10)')
    # ret = db.group_create(group_name,user_list)

    # debug_print('group_create:',ret)

    # ret = db.group_drop(group_name,'yalisa')
    # debug_print('group drop:',ret)
    # for i in range(10):
    #     db.write_cache('yalisa','cache%d'%i)

    # debug_print('read cache:',db.read_cache('yalisa'))
    db.close()