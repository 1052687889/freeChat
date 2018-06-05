from pymysql import *


class DataBase(object):
    def __init__(self):
        self.db = connect(host='127.0.0.1', port=3306, user='root',
                          passwd='123456', db='', charset='utf8')
        self.cursor = self.db.cursor()
        self.cursor.execute(
            "SELECT information_schema.SCHEMATA.SCHEMA_NAME FROM information_schema.SCHEMATA where SCHEMA_NAME='Info';")
        data = self.cursor.fetchall()
        # print(data)
        if not data:
            self.cursor.execute(
                "create database Info default charset=utf8;")  # 创建新库Info
            self.cursor.execute("use Info;")  # 使用新建的Info库
            self.cursor.execute(
                "create table user(id int auto_increment,name varchar(20),password varchar(20),Friends varchar(28),primary key(id))auto_increment=1;")  # 创建user表
        else:
            self.cursor.execute("use Info;")  # 使用Info库
            # 筛选表
            self.cursor.execute(
                "SELECT DISTINCT t.table_name, n.SCHEMA_NAME FROM information_schema.TABLES t, information_schema.SCHEMATA n WHERE t.table_name = 'user' AND n.SCHEMA_NAME = 'Info';")
            data2 = self.cursor.fetchall()
            # print(data2)
            if not data2:
                # 表不存在,创建user表
                self.cursor.execute(
                    "create table user(id int auto_increment,name varchar(20),password varchar(20),Friends varchar(28),primary key(id))auto_increment=1;")


    # 注册
    def submit(self, user, passwd):
        user = str(user)
        passwd = str(passwd)
        sql = "select name from user where name = '" + user + "';"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if not data:  # 用户不存在则新建用户
            sql = "insert into user values(null,'" + \
                user + "','" + passwd + "','" + user + "_friends');"
            # print(sql)
            self.cursor.execute(sql)
            self.db.commit()
            # 创建用户好友表,后缀为_friends
            sql = "create table " + user + \
                "_friends (Friend_name varchar(20));"
            self.cursor.execute(sql)
            return True
        else:
            return False

    # 登录
    def login(self, user, passwd):
        user = str(user)
        passwd = str(passwd)
        # 判断登录名是否在用户表中
        sql = "select password from user where name = '" + user + "';"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data == ():
            return False
        if data[0][0] == passwd:
            return user
        else:
            return False

    # 新建群组
    def create_group(self, gname, member):
        gname = str(gname) + '_group'  # 群组表后缀为_group
        member = set(member)
        if not member:
            return False
        # 判断成员是否全是用户
        L = []
        for i in member:
            sql = "select name from user where name = '" + i + "';"
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            if not data:
                L.append(i)
        if not L:  # 全是用户,判断群组名是否重复
            self.cursor.execute("use Info;")  # 使用Info库
            sql = "SELECT DISTINCT t.table_name, n.SCHEMA_NAME FROM information_schema.TABLES t, information_schema.SCHEMATA n WHERE t.table_name = '" + \
                gname + "' AND n.SCHEMA_NAME = 'Info';"
            self.cursor.execute(sql)
            data2 = self.cursor.fetchall()

            if not data2:  # 组名没有重复,新建群组
                sql = "create table " + gname + " (name varchar(20));"
                self.cursor.execute(sql)  # 创建群组表
                for j in member:
                    sql = "insert into " + gname + " values('" + j + "');"
                    self.cursor.execute(sql)
                    self.db.commit()
                return gname
            # 组名重复
            else:
                return False
        # 给定的member中有非用户
        else:
            return False

    # 删除群组
    def dissolution_group(self, gname):
        groupname = str(gname) + "_group"
        self.cursor.execute("use Info;")  # 使用Info库

        sql = "SELECT DISTINCT t.table_name, n.SCHEMA_NAME FROM information_schema.TABLES t, information_schema.SCHEMATA n WHERE t.table_name = '" + \
            groupname + "' AND n.SCHEMA_NAME = 'Info';"
        # print(sql)
        self.cursor.execute(sql)
        data3 = self.cursor.fetchall()
        if data3:  # 群组存在,删除相应的表
            sql = "drop table " + groupname + " ;"
            # print (sql)
            self.cursor.execute(sql)
            return True
        else:  # 给定的组名不存在
            return False

    # 获取群组成员
    def get_group_member(self, gname):
        groupname = str(gname) + "_group"
        L = []
        self.cursor.execute("use Info;")  # 使用Info库
        # 判断给定的群组是否存在
        sql = "SELECT DISTINCT t.table_name, n.SCHEMA_NAME FROM information_schema.TABLES t, information_schema.SCHEMATA n WHERE t.table_name = '" + \
            groupname + "' AND n.SCHEMA_NAME = 'Info';"
        # print(sql)
        self.cursor.execute(sql)
        data4 = self.cursor.fetchall()
        # 返回群组内的成员列表,群组不存在则列表为空
        if data4:
            sql = "select name from " + groupname + " ;"
            # print (sql)
            self.cursor.execute(sql)
            data5 = self.cursor.fetchall()
            for k in data5:
                L.append(k[0])
        return L

    # 往群组添加成员
    def group_append(self, gname, member):
        groupname = str(gname) + "_group"
        memberlist = []
        # 判断给定member是字符串还是列表
        if type(member) == str:
            memberlist.append(member)
        elif type(member) == list:
            memberlist = member

        L = []  # 存放非用户
        for i in memberlist:
            sql = "select name from user where name = '" + i + "';"
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            # 如果能查到用户名,返回data不为空
            if not data:
                L.append(i)
        # 判断成员是否全是用户
        if not L:  # 全部是用户,加入到群组的表中
            self.cursor.execute("use Info;")  # 使用Info库

            for p in memberlist:  # 判断用户是否已经在群组里,在的直接过掉,不在的就加入
                sql = "select name from " + groupname + " where name = '" + p + "';"
                self.cursor.execute(sql)
                data = self.cursor.fetchall()
                if not data:
                    sql = "insert into " + groupname + " values('" + p + "');"
                    print(sql)
                    self.cursor.execute(sql)
                    self.db.commit()
            return True
        else:  # 有非用户,直接返回False
            return False

    def make_friend(self, userA, userB):
        userA = str(userA)
        userB = str(userB)
        # 判断AB是不是用户
        L = []
        for i in (userA, userB):
            sql = "select name from user where name = '" + i + "';"
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            if not data:
                L.append(i)

        if not L:  # AB均是用户则L为空
            # 判断B是否在A的好友表内
            sql = "select Friend_name from " + userA + \
                "_friends where Friend_name = '" + userB + "';"
            # print(sql)
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            if not data:  # B不在A的好友表内,则加入
                sql = "insert into " + userA + \
                    "_friends values('" + userB + "');"
                # print(sql)
                self.cursor.execute(sql)
                self.db.commit()
            # 判断A是否在B的好友表内
            sql = "select Friend_name from " + userB + \
                "_friends where Friend_name = '" + userA + "';"
            # print(sql)
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            if not data:  # A不在B的好友表内,则加入
                sql = "insert into " + userB + \
                    "_friends values('" + userA + "');"
                # print(sql)
                self.cursor.execute(sql)
                self.db.commit()
            return True
        else:  # AB中有非用户
            return False

    def delete_friend(self, userA, userB):
        userA = str(userA)
        userB = str(userB)
        # 判断AB是不是用户
        Lq = []
        for i in (userA, userB):
            sql = "select name from user where name = '" + i + "';"
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            if not data:
                Lq.append(i)

        if not Lq:
            # 判断B是否在A的好友表内
            sql = "select Friend_name from " + userA + \
                "_friends where Friend_name = '" + userB + "';"
            # print(sql)
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            if not data:
                return False
            else:
                # 将B从A的好友表中删除
                sql = "delete from " + userA + "_friends where Friend_name = '" + userB + "';"
                # print(sql)
                self.cursor.execute(sql)
                self.db.commit()
                # 将A从B的好友表中删除
                sql = "delete from " + userB + "_friends where Friend_name = '" + userA + "';"
                # print(sql)
                self.cursor.execute(sql)
                self.db.commit()
            return True
        else:  # AB中有非用户
            return False

    # 获取好友列表
    def get_friends(self, user):
        user = str(user)
        L = []
        # 判断是不是用户
        sql = "select name from user where name = '" + user + "';"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if not data:  # 用户不存在
            return L
        gname = str(user) + "_friends"
        sql = "select Friend_name from " + gname + ";"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        # print (data)
        for i in data:
            L.append(i[0])
        return L  # 返回用户好友列表


    def __del__(self):
        self.cursor.close()
        self.db.close()


def main():
    A = DataBase()
    for i in range(1, 5):
        name = str(i)
        pw = name + 'aa'
        a = A.submit(name, pw)
        print(a)
    b = A.append_friend(1,6)
    print(b)
    c = A.get_friends(1)
    print(c)


if __name__ == "__main__":
    main()
