# 继承snake_operate.py方法
import sys
import time

import function1.snake_operate as snake_ope
import view.meet_wall_view as mwv
from multiprocessing import Pipe
import threading


class SnakeOperate1(snake_ope.SnakeOperate):

    def __init__(self, snake_entity, food_entity):
        super().__init__(snake_entity, food_entity)

    # 主方法， 负责调用各种必要的方法[使用多线程可能会卡]
    # add_size 蛇吃一个食物增加的长度
    def main(self, w, game_view, second=0.5, add_size=1):
        # 设置蛇吃一次食物增加的长度[与移动的位置有关]
        SnakeOperate1.ADD_SIZE = game_view.ADD_SIZE
        # 设置蛇的形状
        self.snake_entity.set_shape(game_view.SHAPE)

        # 设置蛇的皮肤的颜色
        self.snake_entity.set_skin(game_view.SKIN)

        # 给蛇一个画布, 方便操作
        self.snake_entity.set_w(w)

        # 设置蛇的初始长度
        self.snake_entity.init_body_length(game_view.SNAKE_LENGTH)

        # 显示蛇
        self.show_snake(w)

        # 将 w 传到snake_entity, 方便初始化

        p1, p2 = Pipe()
        t1 = threading.Thread(target=self.snake_all, args=(w, p1, p2, game_view, second))
        t1.setDaemon(True)
        t1.start()

        self.recv_select_info(p1, p2, game_view)

    # 用于蛇的各种控制, 死亡
    def snake_all(self, w, p1, p2, game_view, second):
        while True:
            # self.snake_move(w, p1, p2, second)
            # 用于控制速度
            time.sleep(second)
            # 用于控制移动的位置
            self.snake_move_position()
            # 判断是否吃到食物
            self.is_eat_food(w, game_view)
            # 判断是否碰到墙壁
            self.snake_wall_death(p1, p2)
            # 用于配合self.snake_move_position方法, 形成蛇的移动
            self.snake_place_position(w)
            # 用于判断移动后蛇是否碰到自己的身体
            self.snake_body_death(p1, p2)

    # 专门用于接收用户的选择(重新开始, 退出游戏)
    def recv_select_info(self, p1, p2, game_view):       
        while True:
            result = p2.recv()
            if result == "exit":
                print("退出中")
                game_view.exit_game()
                break
            elif result == "restart":
                print("重新开始游戏")
                game_view.restart_game()
                break
            elif result == "return_game_main":
                print("返回游戏主界面")
                game_view.return_game_main()
                break


    # 离线特有死亡判定方法
    def snake_body_death(self, p1, p2):
        if self.is_move:
            body_position = self.snake_entity.get_body()[0]
            if body_position[-1] in body_position[:-1]:               
                p2.send(self.snake_entity.get_score())
                mwv.MeetWallView().main(p1) 

    # 修改判断是否吃到食物的方法(这需要食物的位置必须和贪吃蛇能到的位置完全一致)
    def is_eat_food(self, w, game_view):
        position_re = self.food_entity.get_position_re()
        snake_position = self.snake_entity.get_position()
        # snake_size = self.food_entity.get_size()
        # 判断是否吃到了食物
        is_eat = False

        # snake_horizontal = snake_position[0] - snake_position[0] % snake_size[0]
        # snake_vertical = snake_position[1] - snake_position[1] % snake_size[1]
        if position_re.get(snake_position) is not None:
            # print("吃到食物了")
            is_eat = True

        # 此方法有太多的无用比较
        # for k in position_re:
        #     if k == snake_position:
        #         # print("吃到食物了")
        #         is_eat = True

        if is_eat:
            # food_position = self.food_entity.get_position()
            # self.food_entity.random_postion()
            # print("吃到食物了")
            # self.food_entity.show_food(w, snake_position)
            self.food_entity.random_show_food(w, position=snake_position)
            for i in range(SnakeOperate1.ADD_SIZE):
                # self.snake_entity.set_body_move(w, self.snake_entity.get_position())
                self.snake_entity.set_body_move(w, self.snake_entity.get_body()[0][-1])

            game_view.grade["text"] = "分数为: %s" % (self.snake_entity.get_score())  