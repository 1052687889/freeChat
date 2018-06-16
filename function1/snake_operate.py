# -*- coding:utf8 -*-

import sys
import time

import entity.snake as snake
import entity.food as food
import view.meet_wall_view as mwv
from multiprocessing import Pipe


class SnakeOperate(object):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    # 吃一个食物增加的长度
    ADD_SIZE = 1


    def __init__(self, snake_entity, food_entity):
        # 保证蛇不能回头， 按的过快， 会使蛇直接原地掉头（处理这个bug的）
        # 进程导致的
        # 默认为零， 表示没有移动， 每改变方向一次，值归 False
        # 改变方向时， 是否有移动一次
        self.is_move = False
        # 保存朝向
        self.direction = None
        self.snake_horizontal = 0
        self.snake_vertical = 0
        self.snake_entity = snake_entity
        self.food_entity = food_entity

    # 主方法， 负责调用各种必要的方法
    def main(self, w, second=0.1):
        while True:
            self.snake_move(w, second)

    # 判定蛇的死亡的方法
    # 碰到墙壁
    def snake_wall_death(self, p1, p2):
        position = self.snake_entity.get_position()
        # 判断是否碰到墙壁
        is_meet_wall = False
        # 判断上的
        if self.direction == SnakeOperate.UP and position[1] < 0:
            is_meet_wall = True
        # 判断下
        elif self.direction == SnakeOperate.DOWN and position[1] \
                - self.snake_entity.game_view_entity.get_height() + self.snake_entity.get_size()[1] > 0:
            is_meet_wall = True

        # 判断左
        elif self.direction == SnakeOperate.LEFT and position[0] < 0:
            is_meet_wall = True

        # 判断右
        elif self.direction == SnakeOperate.RIGHT and position[0] \
                - self.snake_entity.game_view_entity.get_width() \
                * self.snake_entity.game_view_entity.LEFT_RATIO + self.snake_entity.get_size()[1] > 0:
            is_meet_wall = True

        # 碰到墙壁后, 直接发送身体的信息到碰墙的方法那
        if is_meet_wall:
            print("碰到墙壁了")
            p2.send(self.snake_entity.get_score())
            mwv.MeetWallView().main(p1)

    # 蛇的显示
    # 初始化使用
    def show_snake(self, w):
        body_position = self.snake_entity.get_body()[0]
        for bp in body_position:
            # size = self.snake_entity.get_size()
            # re = w.create_rectangle(*bp, bp[0] + size[0], bp[1] + size[1], fill='orange')
            re = self.snake_entity.snake_shape(bp)
            self.snake_entity.set_body(re)
            w.pack()

        # position = self.get_position()
        # size = self.get_size()
        # self.re = w.create_rectangle(*position, position[0] + size[0], position[1] + size[1], fill='orange')
        # w.pack()

    # 控制蛇的方法
    def snake_control(self, event):
        # 用来解决初始化长度不为一, 但状态为已移动的bug
        if self.is_move or self.direction is None:
            self.is_move = False
            horizontal = self.snake_horizontal
            vertical = self.snake_vertical
            if event.char == 'A' or event.char == 'a' and horizontal <= 0:
                horizontal = -self.snake_entity.get_speed_distance()
                vertical = 0
                self.direction = SnakeOperate.LEFT
            elif event.char == 'D' or event.char == 'd' and horizontal >= 0:
                horizontal = self.snake_entity.get_speed_distance()
                vertical = 0
                self.direction = SnakeOperate.RIGHT
            elif event.char == "W" or event.char == 'w' and vertical <= 0:
                vertical = -self.snake_entity.get_speed_distance()
                horizontal = 0
                self.direction = SnakeOperate.UP
            elif event.char == 'S' or event.char == 's' and vertical >= 0:
                vertical = self.snake_entity.get_speed_distance()
                horizontal = 0
                self.direction = SnakeOperate.DOWN
            # elif event.char == " ":
            #     p1, p2 = Pipe()
            #     print("暂停游戏")
            #     p2.send(str(len(self.snake_entity.get_body()[0])) + "stop")
            #     mwv.MeetWallView().main(p1)
            #     # self.snake_entity.
            #     data = p2.recv()
            #     print(data)

            self.snake_horizontal = horizontal
            self.snake_vertical = vertical

    # 判断是否吃到了食物[这个方法只能用于吃单个食物的]
    def is_eat_food(self, w, game_view):
        food_position = self.food_entity.get_position()
        food_size = self.food_entity.get_size()
        snake_position = self.snake_entity.get_position()
        snake_size = self.snake_entity.get_size()
        # print("++++++++++++++++++++++++++++++++++++++++++++++")
        # print("food_position", food_position)
        # print("food_size", food_size)
        # print("snake_position", snake_position)
        # print("++++++++++++++++++++++++++++++++++++++++++++++\n")
        # 判断是否吃到了食物
        is_eat = False
        # 上的判断
        if self.direction == SnakeOperate.UP:
            print("吃到食物了")
            if (0 <= food_position[1] - snake_position[1] < food_size[1]) \
                    and -snake_size[0] < snake_position[0] - food_position[0] < food_size[0]:
                is_eat = True

        # 下的判断
        elif self.direction == SnakeOperate.DOWN:
            if (0 <= snake_position[1] - food_position[1] < food_size[1]) \
                    and -snake_size[0] < snake_position[0] - food_position[0] < food_size[0]:
                is_eat = True

        # 左的判断
        elif self.direction == SnakeOperate.LEFT:
            if (-snake_size[1] < snake_position[1] - food_position[1] < food_size[1]) \
                    and (0 <= snake_position[0] - food_position[0] < food_size[0]):
                is_eat = True

        # 右的判断
        elif self.direction == SnakeOperate.RIGHT:
            if (-snake_size[1] < snake_position[1] - food_position[1] < food_size[1]) \
                    and (0 <= food_position[0] - snake_position[0] < food_size[0]):
                is_eat = True

        if is_eat:
            food_position = self.food_entity.get_position()
            self.food_entity.random_postion()
            # print("吃到食物了")
            self.food_entity.show_food(w, food_position)
            for i in range(SnakeOperate.ADD_SIZE):
                # self.snake_entity.set_body_move(w, self.snake_entity.get_position())
                self.snake_entity.set_body_move(w, self.snake_entity.get_body()[0][-1])

            game_view.grade["text"] = "分数为: %s" % (
                len(self.snake_entity.get_body()[0])-1)


    # 设置蛇的移动后的位置[需要配合snake_place_position使用]
    def snake_move_position(self, w=None, p1=None, p2=None, second=1):
        # time.sleep(second)
        # 用来解决初始化长度不为一, 但状态为已移动的bug
        if self.direction is not None:
            self.is_move = True
        self.snake_entity.set_horizontal(self.snake_entity.get_horizontal() + self.snake_horizontal)
        self.snake_entity.set_vertical(self.snake_entity.get_vertical() + self.snake_vertical)
        self.snake_entity.set_position((self.snake_entity.get_horizontal(), self.snake_entity.get_vertical()))

        # self.is_eat_food(w)
        # self.snake_wall_death(p1, p2)

        # # print(self.snake_entity.get_body()[0])
        # # 把最旧的位置删除，加入一个新的值
        # self.snake_entity.remove_body_head(w)
        # self.snake_entity.set_body_move(w, self.snake_entity.get_position())

        # w.move(re, self.snake_horizontal, self.snake_vertical)

    def snake_place_position(self, w):
        self.snake_entity.remove_body_head(w)
        self.snake_entity.set_body_move(w, self.snake_entity.get_position())
