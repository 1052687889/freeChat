# -*- coding:utf8 -*-


# print("game_view模块导入成功")


class GameViewEntity(object):
    LEFT_RATIO = 0.75
    RIGHT_RATIO = 1 - LEFT_RATIO
    RIGHT_CHILD_TOP_RATIO = 0.7
    RIGHT_CHILD_BOTTOM_RATION = 1 - RIGHT_CHILD_TOP_RATIO

    def __init__(self):
        self.__width = 700
        self.__height = 400
        self.__horizontal = 40
        self.__vertical = 40
        self.__size = (self.__width, self.__height)
        # 待开发
        self.__type = None
        # 设置出现的位置
        self.__position = (self.__horizontal, self.__vertical)

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
        self.set_width(position[0])
        self.set_height(position[1])

    def get_position(self):
        return self.__position


