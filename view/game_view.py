# -*- coding:utf8 -*-
import sys
import tkinter as tk
import threading
from multiprocessing import Process
import time

sys.path.insert(1, "./../")
import entity.game_view as game
import entity.snake as snake
import entity.food as food
import function1.single_snake as snake_operate1
from multiprocessing import Pipe


class PlayMain:

    LEFT_RATIO = game.GameViewEntity.LEFT_RATIO
    RIGHT_RATIO = game.GameViewEntity.RIGHT_RATIO
    RIGHT_CHILD_TOP_RATIO = game.GameViewEntity.RIGHT_CHILD_TOP_RATIO
    RIGHT_CHILD_BOTTOM_RATION = game.GameViewEntity.RIGHT_CHILD_BOTTOM_RATION
    # 刷新速度， 也是蛇的速度
    SPEED = 0.15
    # 蛇一次跑的距离
    SPEED_DISTANCE = 20
    # 食物出现的个数
    COUNT = 5
    # 蛇吃一次食物增加的长度, 与距离有关
    ADD_SIZE = 1
    # 设置蛇的形状, 默认为矩形
    SHAPE = "rectangle"
    # 蛇的所有形状, oval为圆形
    SHAPE_ALL = ("rectangle", "oval")
    # 设置蛇的初始长度
    SNAKE_LENGTH = 1

    # 蛇的皮肤的样式
    SKIN = "random_color"
    SKIN_ALL = ("pink", "green", "random_color")

    # 设置界面的颜色
    GAME_BACKGROUND = "white"
    GAME_BACKGROUND_ALL = {"white":"#EAEDED", "blue":"#21ADF0", "green":"#40DE88"}

    def __init__(self):
        self.w = None
        self.re = None
        self.game_view = tk.Tk()
        self.food_entity = food.FoodEntity()
        self.snake_entity = snake.SnakeEntity()
        # 设置一次跑的距离
        self.game_entity = game.GameViewEntity()

    def main(self, p1):
        # p1 用来告诉主程序是否退出执行
        self.p1 = p1

        # 设置窗口的大小
        self.game_view.geometry('%dx%d' % self.game_entity.get_size())

        self.snake_operate1 = snake_operate1.SnakeOperate1(
            self.snake_entity, self.food_entity)

        self.right_frame = self.create_right_frame(
            *(self.game_entity.get_size()))
        self.create_right_top_frame(self.right_frame)
        self.create_bottom_frame(self.right_frame)
        self.create_left_canvas(self.game_view, *(self.game_entity.get_size()))

        self.snake_entity.set_speed_distance(PlayMain.SPEED_DISTANCE)
        self.game_view.resizable(width=False, height=False)

        t1 = threading.Thread(target=self.snake_operate1.main,
                              args=(self.w, self, PlayMain.SPEED), kwargs={"add_size": PlayMain.ADD_SIZE})
        t1.setDaemon(True)
        t1.start()

        # 显示蛇
        # self.snake_operate1.show_snake(self.w)

        # # 显示食物
        # self.food_entity.random_show_food(
        #     self.w, self.snake_entity.get_position(), count=PlayMain.COUNT)

        # t2 = threading.Thread(target=self.hhh)
        # t2.setDaemon(True)
        # t2.start()

        # print(self.food_entity.random_postion())
        # print(self.food_entity.get_position())

        # 当用户按下按钮时，判断是朝那里的
        print(self.game_view.bind("<Key>", self.snake_operate1.snake_control))
        # t2 = threading.Thread(target=self.snake_entity.snake_move, args=())
        # print("为何没有显示")
        self.game_view.mainloop()
        # 用来表示执行结束了
        self.p1.send("exit_game")
        # print("执行到这了")

    # 设置蛇的速度, 一次跑的距离, 食物的个数
    def snake_config(self, speed=None, speed_distance=None, food_number=None, add_size=None, 
                        shape=None, skin=None, game_background=None, snake_length=None):
        # 速度 >= 0.01
        # 一次移动的距离 <= 20[一个身体的长度, 否则会导致很难迟到食物]
        # 100 >= 食物的个数 >= 1
        # 4 >= 吃一个食物加的长度 >= 0
        if speed is not None and isinstance(speed, (float, int)) \
                and speed >= 0.01 and speed <= 1:
            # 刷新速度， 也是蛇的速度
            PlayMain.SPEED = speed

        if speed_distance is not None and isinstance(speed_distance, int) \
                and speed_distance <= 20:
            # 蛇一次跑的距离
            PlayMain.SPEED_DISTANCE = speed_distance

        if food_number is not None and isinstance(food_number, int) \
                and food_number >= 1 and food_number <= 100:
            # 食物出现的个数
            PlayMain.COUNT = food_number

        if add_size is not None and isinstance(add_size, int) \
                and add_size >= 0 and add_size <= 4:
            # 蛇吃一次食物增加的长度, 与距离有关
            PlayMain.ADD_SIZE = add_size

        if shape is not None and shape in PlayMain.SHAPE_ALL:
            # 设置蛇的形状
            PlayMain.SHAPE = shape

        if skin is not None and skin in PlayMain.SKIN_ALL:
            # 设置蛇的颜色
            PlayMain.SKIN = skin

        if game_background is not None and game_background in PlayMain.GAME_BACKGROUND_ALL.keys():
            # 设置游戏界面的颜色
            PlayMain.GAME_BACKGROUND = game_background

        if snake_length is not None:
            # 设置蛇的初始长度
            PlayMain.SNAKE_LENGTH = snake_length

    # 退出游戏
    def exit_game(self):
        self.p1.send("exit_game")
        self.game_view.destroy()
        # sys.exit()

    # 返回游戏主界面
    def return_game_main(self):
        self.p1.send("return_game_main")
        self.game_view.destroy()

    # 重新开始游戏
    def restart_game(self):
        # print("准备开始游戏")
        self.hhh()
        # print("继续执行中")

        # print("结束了")
        # sys.exit()

    def hhh(self):
        # 用于删除在画布的对应位置的东西
        self.snake_entity.clear_init_body_info(self.w)
        self.food_entity.remove_all_food(self.w)
        # 用于完全初始化数据
        self.food_entity = food.FoodEntity()
        self.snake_entity = snake.SnakeEntity()
        self.game_entity = game.GameViewEntity()
        # 将成绩归零
        self.grade["text"] = "分数为：0"
        self.snake_operate1 = snake_operate1.SnakeOperate1(
            self.snake_entity, self.food_entity)

        self.snake_entity.set_speed_distance(PlayMain.SPEED_DISTANCE)

        self.create_left_canvas(self.game_view, *(self.game_entity.get_size()))

        t1 = threading.Thread(target=self.snake_operate1.main,
                              args=(self.w, self, PlayMain.SPEED))
        t1.setDaemon(True)
        t1.start()
        self.game_view.bind("<Key>", self.snake_operate1.snake_control)

    # 设置初始画布的方法
    def create_left_canvas(self, game_view, wt, ht):
        if self.w is None:
            self.w = tk.Canvas(
                game_view, width=wt*PlayMain.LEFT_RATIO, height=ht, background=PlayMain.GAME_BACKGROUND_ALL[PlayMain.GAME_BACKGROUND])

        # # 显示蛇
        # self.snake_operate1.show_snake(self.w)

        # 显示食物
        self.food_entity.random_show_food(
            self.w, self.snake_entity.get_position(), count=PlayMain.COUNT)

    def create_right_frame(self, wt, ht):
        # print("1")

        right_frame = tk.Frame(
            width=wt*PlayMain.RIGHT_RATIO, height=ht)
        # print("2")
        right_frame.pack(side=tk.RIGHT)
        # print("3")
        return right_frame, wt*PlayMain.RIGHT_RATIO, ht

    def create_right_top_frame(self, right_frame):
        right_top_frame = tk.Frame(master=right_frame[0], width=right_frame[1],
                                   height=right_frame[2]*PlayMain.RIGHT_CHILD_TOP_RATIO, bg="blue")
        right_top_frame.pack(side=tk.TOP)
        self.grade = tk.Label(right_top_frame, text="分数为：%s" % (
            len(self.snake_entity.get_body()[0])-1), font="宋体, 20")
        # label.config(font=("Helvetica -12 bold"))
        # label["text"] = "这也可以!!!"
        self.grade.pack(side=tk.TOP)

        return right_top_frame

    def create_bottom_frame(self, right_frame):
        right_bottom_frame = tk.Frame(master=right_frame[0], width=right_frame[1],
                                      height=right_frame[2] * PlayMain.RIGHT_CHILD_BOTTOM_RATION, bg="orange")
        right_bottom_frame.pack(side=tk.BOTTOM)

        # btn = tk.Button(right_bottom_frame, name="无语中", text="重新开始", command=self.exit_game)
        # btn.pack(side=tk.BOTTOM)

        # btn = tk.Button(right_bottom_frame, name="无语中", text="退出游戏", command=self.restart_game)
        # btn.pack(side=tk.BOTTOM)

        return right_bottom_frame


