# -*- coding:utf8 -*-
# 碰到墙壁的提示

import tkinter
import sys


class MeetWallView:

    # def __init__(self):
        
    #     pass

    def main(self, p1):
        self.p1 = p1
        info = self.p1.recv()
        # 用于判读是否为暂停
        if type(info) is str:
            teshu = info[-4:]
        else:
            teshu = None
        self.view = tkinter.Tk()
        self.view.geometry("300x200")
        tkinter.Frame(self.view, width="300", height="80").pack(side=tkinter.TOP)
        if teshu == "stop":
            # 添加内容
            self.add_hint(self.view, info[:-4])
            # 添加暂停功能[还没有实现]
            self.stop_btn(self.view)
        else:
            # 添加内容
            self.add_hint(self.view, info)
            # 添加退出功能
            self.exit_btn(self.view)
            # 添加再次开始功能
            self.restart_btn(self.view)
            # # 添加返回游戏主界面的功能
            # 有bug
            # self.return_game_main_func(self.view)
        self.view.mainloop()
        # 如果不这样写, 点击X, 会导致无限死循环
        # self.exit_game()
        self.p1.send("exit")
        sys.exit()

    def get_view(self):
        return self.view

    # 添加提示信息
    def add_hint(self, view, info):
        label = tkinter.Label(view, text="分数为：%s" % info, font="宋体, 20")
        # label.config(font=("Helvetica -12 bold"))
        label.pack(side=tkinter.TOP)

    # 添加退出按钮
    def exit_btn(self, view):
        btn = tkinter.Button(view, name="无语中", text="退出游戏", command=self.exit_game)
        btn.pack(side=tkinter.BOTTOM)

    # 添加重新开始按钮
    def restart_btn(self, view):
        btn = tkinter.Button(view, name="重新开始", text="重新开始", command=self.exit_this_view)
        btn.pack(side=tkinter.BOTTOM)

    # 添加返回主界面按钮
    def return_game_main_func(self, view):
        btn = tkinter.Button(view, name="返回主界面", text="返回主界面", command=self.return_game_main)
        btn.pack(side=tkinter.BOTTOM)

    # 添加暂停按钮
    def stop_btn(self, view):
        btn = tkinter.Button(view, name="开始游戏", text="开始游戏", command=self.start_game)
        btn.pack(side=tkinter.BOTTOM)

    # 退出游戏
    def exit_game(self):
        # print("退出游戏")
        self.p1.send("exit")
        self.view.destroy()
        sys.exit()
        # self.view.quit()
        # return "exit"

    # 重新开始游戏
    def exit_this_view(self):
        # print("重新开始游戏")
        self.p1.send("restart")
        self.view.destroy()
        sys.exit()
        # self.view.quit()

    # 退回到游戏主界面
    def return_game_main(self):
        # print("返回主界面中")
        self.p1.send("return_game_main")
        self.view.destroy()
        sys.exit()

    # 再次开始游戏
    def start_game(self):
        self.p1.send("start")
        self.view.destroy()
        sys.exit()

# if __name__ == "__main__":
#     MeetWallView().main()
