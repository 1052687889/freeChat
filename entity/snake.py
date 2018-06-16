# -*- coding:utf8 -*-

import entity.food as food
import entity.game_view as game_view
import random
from tkinter import *
# from PIL import Image
# print("snake模块导入成功")


class SnakeEntity:
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    # 设置蛇的身体的形状
    SHAPE_ALL = {"rectangle":None, "oval":None}
    # 设置蛇的身体的颜色
    SKIN_ALL = ("pink", "green", "random_color")

    def __init__(self):
        self.food_entity = food.FoodEntity()
        self.game_view_entity = game_view.GameViewEntity()

        # 设置初始速度(必须是块大小的倍数)
        self.__speed_distance = 20
        # 这是指单个身体的长度
        self.__length = 20
        self.__height = 20
        self.__horizontal = 40
        self.__vertical = 40
        self.__size = (self.__length, self.__height)
        # 用于初始化身体数据的
        self.__init_body = [[(20, 40)], []]
        # 待开发
        self.__type = None
        self.__position = (self.__horizontal, self.__vertical)
        # 初始身体的位置[默认是一个]，以及块数
        self.__body = [[(40, 40)], []]
        # 设置身体的形状
        self.__shape = "rectangle"
        # 设置蛇的皮肤的颜色
        self.__skin = "random_color"
        # 画布, 用于蛇的一些方法的初始化使用
        self.__w = None
        # 蛇的长度, 默认为1
        self.length = 1

    def set_speed_distance(self, speed_distance):
        self.__speed_distance = speed_distance

    def get_speed_distance(self):
        return self.__speed_distance

    def set_length(self, length):
        self.__length = length

    def get_length(self):
        return self.__length

    def set_height(self, height):
        self.__height = height

    def get_height(self):
        return self.__height

    def set_size(self, size):
        self.__size = size

    def get_size(self):
        return self.__size

    def set_horizontal(self, horizontal):
        self.__horizontal = horizontal

    def get_horizontal(self):
        return self.__horizontal

    def set_vertical(self, vertical):
        self.__vertical = vertical

    def get_vertical(self):
        return self.__vertical

    def set_position(self, position):
        self.__position = position
        self.set_horizontal(position[0])
        self.set_vertical(position[1])

    def get_position(self):
        return self.__position

    def set_body(self, re, position=None):
        if position is not None:
            self.__body[0].append(position)
        self.__body[1].append(re)

    def get_body(self):
        return self.__body

    def set_shape(self, shape):
        if shape in SnakeEntity.SHAPE_ALL:
            self.__shape = shape

    def get_shape(self):
        return self.__shape

    def set_skin(self, skin):
        if skin in SnakeEntity.SKIN_ALL:
            self.__skin = skin

    def get_skin(self):
        return self.__skin

    def set_w(self, w):
        self.__w = w
        self.init_SHAPE_ALL()

    # 返回蛇的分数(经过处理)
    def get_score(self):
        return len(self.get_body()[0]) - self.length

    # 专门设置身体的初始长度[默认为1]
    def init_body_length(self, length):
        if length >= 1:           
            for _ in range(length-1):
                self.__body[0].append(self.get_position())
            self.length = length

    # 初始化蛇的形状, 以及对应的方法,
    # 就是初始化 SHAPE_ALL
    # 这里有较大的bug, 需要改进
    def init_SHAPE_ALL(self):
        SnakeEntity.SHAPE_ALL["rectangle"] = self.__w.create_rectangle
        SnakeEntity.SHAPE_ALL["oval"] = self.__w.create_oval

    # 蛇的形状的方法
    def snake_shape(self, position):
        size = self.get_size()

        shape = self.get_shape()
        # 选择蛇的颜色
        skin = self.get_skin()
        re = None
        if skin == "random_color":
            # 产生随机的六位的颜色
            color = "#"
            for i in range(6):
                color += str(random.randrange(0, 10))
        else:
            color = skin

        # 选择蛇的身体的形状
        if SnakeEntity.SHAPE_ALL.get(shape) is not None:
            re = SnakeEntity.SHAPE_ALL.get(shape)(*position, position[0]+size[0], position[1]+size[1],
                                    fill=color)
        return re

    # 移除第一个身体, 用于身体的移动
    def remove_body_head(self, w):
        self.__body[0].pop(0)
        w.delete(self.__body[1][0])
        w.pack()
        self.__body[1].pop(0)

    # 蛇的显示
    # 初始化使用
    # def show_snake(self, w):
    #     body_position = self.get_body()[0]
    #     for bp in body_position:
    #         size = self.get_size()
    #         re = w.create_rectangle(*bp, bp[0] + size[0],
    #                                 bp[1] + size[1], fill='write')
    #         self.snake_entity.set_body(re)
    #         w.pack()

    # 身体的移动
    def set_body_move(self, w, position):
        self.__body[0].append(position)
        size = self.get_size()
        color = ""
        shape = self.get_shape()

        # 选择蛇的颜色
        # skin = self.get_skin()
        # if skin == "random_color":
        #     # 产生随机的六位的颜色
        #     color = "#"
        #     for i in range(6):
        #         color += str(random.randrange(0, 10))
        # else:
        #     color = skin
        # fill='#%s' % color
        # myImage = PhotoImage(file="/home/tarena/桌面/课程学习/小组项目/功能/多人在线贪吃蛇/单人离线贪吃蛇/单人离线贪吃蛇优化版/entity/20.gif")
        # image = Image.open("/home/tarena/桌面/课程学习/小组项目/功能/多人在线贪吃蛇/单人离线贪吃蛇/单人离线贪吃蛇优化版/entity/bg2.jpg")
        # print(image)
        # myImage = image.convert("LA")
        # print(myImage)
        # w.create_image(100, 200, anchor=NW,
        #                         image=image)

        re = self.snake_shape(position)
        # 选择蛇的身体的形状
        # if SnakeEntity.SHAPE_ALL.get(shape) is not None:
        #     # 矩形
        #     re = SnakeEntity.SHAPE_ALL.get(shape)(*position, position[0]+size[0], position[1]+size[1],
        #                             fill=color)
        # elif shape == "oval":
        #     # 圆形
        #     re = w.create_oval(*position, position[0]+size[0], position[1]+size[1],
        #                             fill=color)

        # 三角形
        # re = w.create_rectangle(*position, position[0]+size[0], position[1]+size[1],
        #                         fill="pink")

        self.__body[1].append(re)
        w.pack()

    # 清空所有身体信息, 初始化位置
    def clear_init_body_info(self, w):
        for gb in self.get_body()[1]:
            w.delete(gb)
        w.pack()
        self.__body = self.__init_body

    # def add_body_child(self, w, position):
    #     self.__body[0].append(position)
    #     size = self.get_size()
    #     re = w.create_rectangle(*position, position[0] + size[0], position[1] + size[1], fill='orange')
    #     self.__body[1].append(re)
    #     w.pack()
