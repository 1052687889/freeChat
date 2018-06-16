#coding:utf-8
import struct
import re
import queue
import threading
from time import *
from crc16 import *
from json import *
from traceback import *
#该装饰器会按错误的格式打印错误，但是程序不会崩溃
def except_catcher(func):
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception as e:
            print_exc()
    return wrapper



def formattime(time):
    return strftime('%Y-%m-%d %X',gmtime(time))

class Data(object):
    @classmethod
    def parse(cls,dtype,data):
        if dtype == 'json':
            data = loads(data)
        else:
            pass
        return data        

class DataProcessing(object):
    def __init__(self):
        pass

    @classmethod
    def addlen(cls,bytedata,n):
        #把字节串的长度转为n位16进制字节串并放在byte之前，例 f(b'rt') = b'2rt'
        return (('%0'+str(n)+'x')%len(bytedata)).encode() + bytedata

    @classmethod
    def getlen(cls,bytedata,n):
        #上述匿名函数的逆过程,并把多余字节串返回。例 f(b'2rtty') = b'rt',b'ty'
        l = int(bytedata[:n],16)
        return bytedata[n:l+n],bytedata[l+n:]

    @classmethod
    def encode(cls,source,target,time,dtype,data):
        if dtype != 'bytes':
            data = data.encode()

        sour = source().encode()
        targ = target().encode()
        dtyp = dtype.encode()
        length = (len(sour),len(targ),len(dtyp),len(data))
        buf = struct.pack('!BBBH',*length)
        buf2 = struct.pack('!d%ds%ds%ds%ds'%length,time,sour,targ,dtyp,data)
        return buf+buf2

    @classmethod
    def decode(cls,bytedata):
        length = struct.unpack_from('!BBBH',bytedata)
        data = struct.unpack_from('!d%ds%ds%ds%ds'%length,bytedata,5)
        
        time   = data[0]
        source = UserID(data[1].decode())
        target = UserID(data[2].decode())
        dtype  = data[3].decode()
        if dtype != 'bytes':
            data = data[4].decode()

        return source,target,time,dtype,data

    @classmethod
    def decryption(cls,ciphertext):
        return ciphertext
        #return plaintext

    @classmethod
    def encryption(cls,plaintext):
        return plaintext
        #return ciphertext

#   帧头   负载长度   负载   CRC16校验
#  1Byte    6Byte    nByte   4Byte
    @classmethod
    def pack(cls,source,target,dtype,data,time = time()):

        sendata = (source,target,time,dtype,data)
        encr_bytes = cls.encryption(cls.encode(*sendata))

        x = bytes.fromhex('AA') + cls.addlen(encr_bytes,6) + CRC16(encr_bytes)

        return x
        #return bytes.fromhex('AA') + cls.addlen(encr_bytes,6) + CRC16(encr_bytes)

    @classmethod
    def unpack(cls,data):
        ''' 数据包的长度不一定正好能够解开
            也不一定解开后刚好无剩余
            所以返回的第一个变量表示剩余数据，无则返回空字节串
            第二个变量返回解出的内容，无则返回空列表
            第三个变量用于指示当前解包是否成功
            但是解包过程出错未做处理
        '''
        #数据必须以0XAA开头
        data = data[data.find(bytes.fromhex('AA')):] 

        datacount = len(data)

        #至少要10个字节
        if datacount < 10:
            return data,[],False

        #提取负载
        length = int(data[1:7],16)

        #帧长度大于数据长度，说明可能由于某种情况导致数据未接收完成
        if length+9 > datacount :
            #print('length,datacount',length+9, datacount)
            return data,[],False

        #提取有效负载
        payload,surplus = cls.getlen(data[1:],6)
        
        #提取CRC值
        crcvalue = surplus[:4]
        surplus  = surplus[4:]

        #CRC校验出错，丢弃该数据包
        if CRC16(payload) != crcvalue:
            print('crc error',CRC16(payload),crcvalue)
            return surplus,[],True
        return surplus,cls.decode(cls.decryption(payload)),True

class RcvDataProcessing(object):
    def __init__(self):
        self.packed_data = b''

    def processing(self,packed_data,commandfunc):
        self.packed_data += packed_data
        while True:
            #print(self.packed_data)
            self.packed_data,content,result = DataProcessing.unpack(self.packed_data)
            if result == False:
                break

            if content != []:
                commandfunc(*content)
            else:
                #print('receive data is empty',content)
                pass
#目标和源ID解析
class UserID(object):
    def __init__(self,dtype,name = None):
        if isinstance(dtype,UserID):
            self.dtype= dtype.dtype
            self.name = dtype.name

        elif ',' in dtype:
             self.dtype,self.name = dtype.split(',')
        else:
            self.dtype = dtype
            self.name = name


    def __repr__(self):
        if self.name is None:
            return "UserID('%s')"%(self.dtype)
        else:
            return "UserID('%s','%s')"%(self.dtype,self.name)

    def __str__(self):
        if self.name is None:
            return str(self.dtype)
        else:
            return str('%s,%s'%(self.dtype,self.name))

    def __call__(self):
        '''把该对象转为字符串'''
        if self.name is None:
            return self.dtype
        else:
            return ("%s,%s"%(self.dtype,self.name))

from time import *

def subcommandhandle(join=None,allusers=None,count = None):
    print('join:',join)
    print('allusers:',allusers)
    print('count:',count)


def commandhandle(argdict):
    if 'join' in argdict:
        subcommandhandle(**argdict)
    else:
        print('cmdhandle',argdict)
        
if __name__ == '__main__':

    encodedata = b''
    #encodedata = b'000037000604user23001704time2018-05-14 20:08:38000804data123\n'
    encodedata += DataProcessing.pack({'join':b'123','count':b'123','allusers':b''})
    encodedata += DataProcessing.pack({'data':b'ffjpjapf','allusers':b''})
    rcvdatapro = RcvDataProcessing(commandhandle)
    rcvdatapro.processing(encodedata)
