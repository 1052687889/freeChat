# 使用tcp协议传输数据
import socket
import sys
import getpass


# sys.stdin.flush()   # 清除标准输入的缓存

class ElecDictClient:
    HOST = "127.0.0.1"
    PORT = 8888
    ADDR = (HOST, PORT)

    def __init__(self):

        # 创建套接字
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.s.connect(ADDR)

    def main(self):
        self.connect_server()

    # 总的功能显示
    def show(self):
        print("++++++++++ 1)贪吃蛇 +++++++++++")
        print("++++++++++ 2)退出 +++++++++++")

    # 连接服务端, 并且发送请求信息到服务端
    def connect_server(self):
        while True:
            self.show()
            request = input("请输入对应的序号: ")
            if request == "1":
                self.login()
            elif request == "2":
                self.register()
            # elif request == "3":
            #     self.find()
            elif request == "4":
                self.s.send(b"E")
                sys.exit()
            else:
                print("输入有误, 请重新输入")

    def __del__(self):
        self.s.close()


def main():
    ElecDictClient().main()


if __name__ == "__main__":
    main()