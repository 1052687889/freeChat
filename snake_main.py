# -*- coding: utf-8 -*-
import os
import view.game_view as gv
import view.snake_config_view as scv
import view.main_view as mv
from multiprocessing import Pipe
from const import *
from threading import Thread

def send_exit_msg(queue):
    msg = MsgType(type=MsgType.MSG_SNACK, msgtype=MsgType.CLOSE_DLG, msg=os.getpid())
    queue.put(msg)

def main(queue):
    # 用于获得信息 scv 或 mv 传过来的信息
    p1, p2 = Pipe()
    gv1 = gv.PlayMain()
    while True:
        # 启动主界面
        mv.main(p1,queue)
        # print("执行下面的")
        data = p2.recv()
        # print("数据:", data)
        if data == "start":
            pass
        elif data == "config_start":
            # 需要有一个选择的界面
            # 清空多余的数据
            p2.recv()
            scv.main(p1,queue)
            data = p2.recv()
            # print("数据为： ", data)
            if data == "return_game_main":
                # 把 管道中的数据清空
                p2.recv()
                continue
            elif data == "exit_game":
                send_exit_msg(queue)
                break
            # 设置一些初始属性,
            # 速度 >= 0.01
            # 一次移动的距离 <= 20[一个身体的长度, 否则会导致很难吃到食物]
            # 100 >= 食物的个数 >= 1
            # 4 >= 吃一个食物加的长度 >= 0
            # 蛇的身体的形状
            # 蛇的皮肤的颜色
            # 设置游戏的背景色
            # 设置蛇的长度
            else:
                # 需要清空数据
                gv1.snake_config(**data)
                # 清空数据
                p2.recv()
            # gv1.snake_config(0.05, "银河壹号", "怪物猎人", "女巫", "oval", "pink", "white", 10)
        elif data == "exit_game":
            send_exit_msg(queue)
            # print("退出游戏")
            break

        gv1.main(p1)
        # print("往下走了")
        data = p2.recv()
        if data == "exit_game":
            send_exit_msg(queue)
            break
        elif data == "return_game_main":
            continue
        else:
            send_exit_msg(queue)
            # print("游戏出错了")
            break


# if __name__ == "__main__":
#     main()

