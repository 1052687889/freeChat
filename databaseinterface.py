# coding:utf-8
from pymysql import *
import re

def debug_print(*args,**kwargs):
    #print(*args,**kwargs)
    pass
from traceback import print_exc
class DataBaseInterface(object):

    def __init__(self, user, passwd,
                 host='127.0.0.1', port=3306,
                 db='', charset='utf8'):

        self.db = connect(host=host, port=port,
                          user=user, passwd=passwd,
                          db=db, charset=charset)
        self.cursor = self.db.cursor()
        #self.database = _DataBase(self.cursor)


# create table test1(id int auto_increment primary key,name
# char(20))auto_increment=10000;
    def test(self):
        self.create('dict.test3', {
                    'id': 'int', 'name': 'char(20)'}, primary='id', auto_increment=1000)

    def __create_table_sql(self, tablename, values, primary=None, auto_increment=None):
        def pack_key(key, ktype, primary=None, auto_increment=None):

            if primary != key:
                return ' '.join([key, ktype])
            if auto_increment == None:
                return ' '.join([key, ktype, 'primary key'])
            else:
                return ' '.join([key, ktype, 'auto_increment', 'primary key'])
        if isinstance(values, str):
            value_list = [pack_key(*values.split(' '), primary, auto_increment)]
        else:
            value_list = [pack_key(*v.split(' '), primary, auto_increment) for v in values]

        tablevalue = '({})'.format(','.join(value_list))
        if auto_increment is not None:
            tablevalue += 'auto_increment={}'.format(auto_increment)

        return 'create table {}{};'.format(tablename, tablevalue)

    def create(self, name, values_dict=None, primary=None, auto_increment=None):
        '''创建库或表,表暂时只支持主键和自增长属性'''
        try:
            if '.' not in name:
                self.cursor.execute(
                    'create database {} default charset = utf8;'.format(name))
            else:
                database, table = name.split('.')
                self.use(database)
                if values_dict is None:
                    raise ValueError(
                        'ERROR 1113 (42000): A table must have at least 1 column')
                debug_print('create:', self.__create_table_sql(
                    table, values_dict, primary, auto_increment))
                self.cursor.execute(self.__create_table_sql(
                    table, values_dict, primary, auto_increment))

            return self
        except Exception as e:
            debug_print('Error:', e)

    def create_if_not_exist(self, name, values_dict=None, primary=None, auto_increment=None):
        if not self.is_exist(name):

            self.create(name, values_dict = values_dict,
                        primary=primary, auto_increment=auto_increment)
    def drop(self, name):
        '''删除库或表'''
        try:
            if '.' not in name:
                self.cursor.execute('drop database {};'.format(name))
            else:
                database, table = name.split('.')
                self.use(database)
                self.cursor.execute('drop table {};'.format(table))
            return self
        except Exception as e:
            debug_print('Error:', e)

    def show(self, name=-1):
        '''SQL语法 show'''
        if name == -1:
            self.cursor.execute('show databases;')
            return self.cursor.fetchall()
        else:
            try:
                self.cursor.execute('show create database {};'.format(name))
                return self.cursor.fetchall()
            except Exception as e:
                debug_print(e)

    def use(self, name):
        '''使用库'''
        try:
            self.cursor.execute('use {}'.format(name))
            return self
        except Exception as e:
            debug_print('Error:', e)

    def is_exist(self, name):
        '''判断库或表是否存在'''
        if '.' in name:
            database, table = name.split('.')
            ret = self.show_tables(database)
            return bool((table,) in ret)

        else:
            try:
                self.cursor.execute('show create database {};'.format(name))
                self.cursor.fetchall()
                return True
            except:
                return False

    def show_tables(self, name):
        '''显示库中所有表'''
        try:
            self.use(name)
            self.cursor.execute('show tables;')
            return self.cursor.fetchall()
        except Exception as e:
            debug_print('Error:', e)

    def commit(self):
        '''提交事务'''
        self.db.commit()

    def insert(self, name, args_list):
        '''往表中插入值'''

        # 解析参数
        def arg_parse(arg):
            if arg is None:
                return 'null'
            elif isinstance(arg, str):
                return arg.__repr__()
            else:
                return str(arg)

        value = ','.join([arg_parse(arg) for arg in args_list])

        try:
            database, table = name.split('.')
            self.use(database)
            debug_print("insert into {} values({});".format(table, value))
            self.cursor.execute(
                "insert into {} values({});".format(table, value))
            return self
        except Exception as e:
            debug_print('Error:', e)
            print_exc()

    def desc(self, name):
        '''查看表结构'''
        try:
            database, table = name.split('.')
            self.use(database)

            self.cursor.execute('desc {};'.format(table))
            return self.cursor.fetchall()
        except Exception as e:
            debug_print('Error:', e)

    def close(self):

        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

    def select(self, name, field='*', where=None):
        '''查找语句'''
        try:
            database, table = name.split('.')
            self.use(database)
            if where is not None:
                debug_print('select {} from {} where {};'.format(field, table, where))
                self.cursor.execute(
                    'select {} from {} where {};'.format(field, table, where))
            else:
                debug_print('select {} from {};'.format(field, table))
                self.cursor.execute('select {} from {};'.format(field, table))

            return self.cursor.fetchall()

        except Exception as e:
            debug_print('Error:', e)

    def delete(self, name, where=None):
        '''删除表中的数据'''
        database, table = name.split('.')
        self.use(database)
        if where is not None:
            print('delete from {} where {};'.format(table, where))
            self.cursor.execute(
                'delete from {} where {};'.format(table, where))
            return self
        else:
            self.cursor.execute('delete from {};'.format(table))
            return self
    #update 表名 set 字段名=值1,... where 条件;
    def update(self,name,values,where=None):

        database, table = name.split('.')
        self.use(database)

        where = ';' if where is None else 'where {} ;'.format(where)
        values = ','.join(values)
        print('update {} set {} '.format(table, values)+where)
        self.cursor.execute('update {} set {} '.format(table, values)+where)
        return self

    def get_count(self, name):
        '''获取表中记录总条数'''

        return self.select(name, field='count(*)')[0][0]


if __name__ == "__main__":
    database = DataBaseInterface('root', '123456')

    # 创建　库
    if not database.is_exist('dict1'):
        database.create('dict1')

    # #删除库
    # if database.is_exist('dict1'):
    #     database.drop('dict1')

    # 删除表
    # if database.is_exist('dict1.test10'):
    #     database.drop('dict1.test10')

    # 创建表
    if not database.is_exist('dict1.test10'):
        database.create('dict1.test10', ('id int', 'name char(20)',
                                         'age int'), primary='id', auto_increment=1)

        # #创建只有一个元素的表
        # database.create('dict1.test10','id int')

    # 往表中插入数据,其中 commit()方法可以另外调用，或者这样链式调用
    database.insert('dict1.test10', [None, 'antony', 12]).commit()

    # #查询表中所有数据
    # ret = database.select('dict1.test10')
    # debug_print(ret)

    # #查询id>5的姓名和年龄
    # ret = database.select('dict1.test10',field = 'name,age',where = 'id<5')
    # debug_print(ret)

    # #查询表结构
    # ret = database.desc('dict1.test10')
    # debug_print(ret)

    # 查询数据总数
    debug_print('数据总条数：', database.get_count('dict1.test10'))

    # 删除id为1的数据
    database.delete('dict1.test10', where='id=1').commit()

    # 显示所有库
    debug_print('所有库：', database.show())

    # 显示指定库
    debug_print('指定库: ', database.show('dict1'))

    debug_print('库中所有表:', database.show_tables('dict1'))
    database.close()
