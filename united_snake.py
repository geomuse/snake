import gym
from gym import spaces
import pygame
import time
import random
import numpy as np

class SnakeEnv(gym.Env):
    def __init__(self):
        super(SnakeEnv, self).__init__()
        pygame.font.init()
        # 游戏窗口大小和速度设置
        self.window_width = 800
        self.window_height = 600
        self.snake_block = 10
        self.snake_speed = 15

        # 定义颜色
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.purple = (155, 89, 182)
        self.green = (46, 204, 113)
        self.blue = (52, 152, 219)

        # 定义动作空间和状态空间
        self.action_space = spaces.Discrete(4)  # 上、下、左、右
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.window_height, self.window_width, 3), dtype=np.uint8)

        self.game_window = None
        self.snake_list = []
        self.snake_length = 1
        self.snake_x = self.window_width / 2
        self.snake_y = self.window_height / 2
        self.snake_x_change = 0
        self.snake_y_change = 0
        self.food_x = round(random.randrange(0, self.window_width - self.snake_block) / 20.0) * 20.0
        self.food_y = round(random.randrange(0, self.window_height - self.snake_block) / 20.0) * 20.0
        self.clock = pygame.time.Clock()

    def _init_windows(self):
        # 创建游戏窗口
        self.game_window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('贪吃蛇游戏')

    def design_snake(self, snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.game_window, self.green, [x[0], x[1], snake_block, snake_block])

    def display_score(self, score):
        font = pygame.font.SysFont(None, 15)
        text = font.render(str(score), True, self.blue)
        self.game_window.blit(text, [10, 10])

    def score_table_show(self):
        # 显示游戏结束信息
        font_style = pygame.font.SysFont(None, 15)
        message = font_style.render(str(self.snake_length - 1), True, self.black)
        self.game_window.blit(message, [self.window_width / 2, self.window_height / 2])
        pygame.display.update()
        time.sleep(2)  # 等待2秒后退出游戏

    def reset(self):
        self._init_windows()
        self.snake_list = []
        self.snake_length = 1
        self.snake_x = self.window_width / 2
        self.snake_y = self.window_height / 2
        self.snake_x_change = 0
        self.snake_y_change = 0
        self.food_x = round(random.randrange(0, self.window_width - self.snake_block) / 20.0) * 20.0
        self.food_y = round(random.randrange(0, self.window_height - self.snake_block) / 20.0) * 20.0

        observation = self.get_observation()
        return observation

    def step(self, action):
        if action == 0:
            self.snake_y_change = -self.snake_block
            self.snake_x_change = 0
        elif action == 1:
            self.snake_y_change = self.snake_block
            self.snake_x_change = 0
        elif action == 2:
            self.snake_x_change = -self.snake_block
            self.snake_y_change = 0
        elif action == 3:
            self.snake_x_change = self.snake_block
            self.snake_y_change = 0

        self.snake_x += self.snake_x_change
        self.snake_y += self.snake_y_change

        done = False
        reward = 0

        if self.snake_x >= self.window_width or self.snake_x < 0 or self.snake_y >= self.window_height or self.snake_y < 0:
            self.score_table_show()
            done = True
            reward = -10

        if [self.snake_x, self.snake_y] in self.snake_list[:-1]:
            self.score_table_show()
            done = True
            reward = -10

        self.game_window.fill(self.white)
        pygame.draw.rect(self.game_window, self.purple, [self.food_x, self.food_y, self.snake_block, self.snake_block])
        snake_head = []
        snake_head.append(self.snake_x)
        snake_head.append(self.snake_y)
        self.snake_list.append(snake_head)
        if len(self.snake_list) > self.snake_length:
            del self.snake_list[0]

        self.design_snake(self.snake_block, self.snake_list)
        self.display_score(self.snake_length - 1)
        pygame.display.update()

        if self.snake_x == self.food_x and self.snake_y == self.food_y:
            self.food_x = round(random.randrange(0, self.window_width - self.snake_block) / 20.0) * 20.0
            self.food_y = round(random.randrange(0, self.window_height - self.snake_block) / 20.0) * 20.0
            self.snake_length += 1
            reward = 10

        observation = self.get_observation()
        return observation, reward, done, {}

    def get_observation(self):
        observation = pygame.surfarray.array3d(pygame.display.get_surface())
        observation = np.transpose(observation, axes=(1, 0, 2))
        return observation

    def render(self, mode='human'):
        # 在屏幕上显示游戏状态
        self.game_window.fill(self.white)
        pygame.draw.rect(self.game_window, self.purple, [self.food_x, self.food_y, self.snake_block, self.snake_block])
        self.design_snake(self.snake_block, self.snake_list)
        self.display_score(self.snake_length - 1)
        pygame.display.update()
        self.clock.tick(self.snake_speed)

        # 等待玩家操作
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_UP:
                    return 0  # 上
                elif event.key == pygame.K_DOWN:
                    return 1  # 下
                elif event.key == pygame.K_LEFT:
                    return 2  # 左
                elif event.key == pygame.K_RIGHT:
                    return 3  # 右

    def close(self):
        pygame.quit()
        quit()

if __name__ == "__main__":
    env = SnakeEnv()
    observation = env.reset()
    done = False

    while not done:
        action = env.render()  # 人类模式下，玩家通过键盘操作
        observation, reward, done, _ = env.step(action)