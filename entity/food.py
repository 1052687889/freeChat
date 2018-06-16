# -*- coding:utf8 -*-

from random import randrange
import entity.game_view as game_view
import time
# print("food模块导入成功")


class FoodEntity:

    def __init__(self):
        self.__width = 20
        self.__height = 20
        self.__horizontal = 10 * self.__width
        self.__vertical = 7 * self.__height
        self.__size = (self.__width, self.__height)
        # 待开发
        self.__type = None
        # 食物的位置
        self.__position = (self.__horizontal, self.__vertical)
        # 食物在画布中对应的 值 的 列表
        self.__position_re = {}
        self.game_view_entity = game_view.GameViewEntity()

    # 食物的随机出现
    def random_show_food(self, w, snake_start_position=None, count=1, position=None):
        while count >= 1:
            # 初始化时，需要确定食物不出现在蛇的位置， 之后不用判断
            self.random_postion(snake_start_position)
            self.show_food(w, position)
            count -= 1

    # 食物的随机位置(不能是蛇所在的位置， 否则由于蛇不动， 会导致出现直接死亡的情况)
    def random_postion(self, snake_start_position):
        # 这是整个游戏的尺寸， 需要的是游戏的界面
        while True:
            width = self.game_view_entity.get_width() * self.game_view_entity.LEFT_RATIO
            height = self.game_view_entity.get_height()
            horizontal = randrange(80, width - self.get_size()[0], self.get_size()[0])
            vertical = randrange(0, height, self.get_size()[1])
            # 判断是否是蛇的位置， 是则重新获得新的位置
            if snake_start_position is not None and snake_start_position == (horizontal, vertical):
                continue
            # 这是用于去重复位置的
            if self.get_position_re().get((horizontal, vertical)) is None:
                # 这是用于食物的稀疏的
                meet_condition = 0
                if self.get_position_re().get((horizontal + 20, vertical)) is not None:
                    meet_condition += 1 
                if self.get_position_re().get((horizontal, vertical + 20)) is not None:
                    meet_condition += 1
                if self.get_position_re().get((horizontal - 20, vertical)) is not None:
                    meet_condition += 1
                if self.get_position_re().get((horizontal, vertical - 20)) is not None:
                    meet_condition += 1
                # print(meet_condition)
                if meet_condition <= 1:
                    break

                
            # if horizontal != self.get_horizontal() or vertical != self.get_vertical():
            #     break
        self.set_horizontal(horizontal)
        self.set_vertical(vertical)
        self.set_position((horizontal, vertical))
        # print(self.get_position())
        # return horizontal, vertical

    # 食物的出现 (根据 position 确认位置), 顺带删除之前的食物
    def show_food(self, w, position=None):
        # print(FoodEntity.RE)
        # position 是表示蛇所吃到的食物的位置， 默认为None
        position_re = self.get_position_re()
        if position_re:
            # print(position_re.get(position))
            # print(self.get_position())
            w.delete(position_re.get(position))
            self.remove_position_re(position)
        position = self.get_position()
        size = self.get_size()
        re = w.create_rectangle(*position, position[0] + size[0]
                                                   , position[1] + size[1], fill='red')
        self.set_position_re(position, re)
        # print(self.get_position_re())
        w.pack()

    def set_height(self, height):
        self.__height = height

    def get_height(self):
        return self.__height

    def set_width(self, width):
        self.__width = width

    def get_width(self):
        return self.__width

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

    def set_position_re(self, position, re):
        self.__position_re[position] = re

    def get_position_re(self):
        return self.__position_re

    # 移除指定位置的值
    def remove_position_re(self, position):
        if self.__position_re.get(position):
            del self.__position_re[position]

    # 移除所有的值
    def remove_all_food(self, w):
        # print(len(self.__position_re.items()))
        for k, v in self.__position_re.items():
            w.delete(v)
        self.__position_re = {}
        w.pack()
