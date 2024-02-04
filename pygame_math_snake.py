import pygame
import time
import random
import numpy as np
from dataclasses import dataclass

@dataclass
class snake :
    pygame.font.init()
    # 游戏窗口大小和速度设置
    window_width = 800
    window_height = 600
    snake_block = 10
    snake_speed = 15
    
    # 定义颜色
    black = (0, 0, 0)
    white = (255, 255, 255)
    
    purple = (155, 89, 182)
    carrot = (230, 126, 34)
    silver = (189, 195, 199)
    concrete = (149, 165, 166)
    sun_flower = (241, 196, 15)
    green_sea = (22, 160, 133)

    green = (46, 204, 113)

    turquoise = (26, 188, 156)
    blue = (52, 152, 219)

    game_window = None
    snake_list = []
    snake_length = 1
    snake_x = window_width / 2
    snake_y = window_height / 2
    snake_x_change = 0
    snake_y_change = 0
    food_x1 = None
    food_y1 = None
    food_x2 = None
    food_y2 = None
    food_font = pygame.font.SysFont(None, 20)
    clock = pygame.time.Clock()
    action = None

    def _init_windows(self):
        # 创建游戏窗口
        self.game_window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('snake.')

    def design_snake(self, snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.game_window, self.green, [x[0], x[1], snake_block, snake_block])

    def generate_question(self):
        x = random.randint(0,100)
        y = random.randint(0,100)
        z = random.randint(0,100)
        self.x , self.y , self.z = x , y , z
    
    def generate_question_string(self):
        return f'{self.x}+{self.y}=?'
    
    def generate_random_answer(self):
        return self.z+self.y

    def generate_true_answer(self):
        return self.x+self.y

    def choose_color(self):
        color = random.sample([self.purple,self.carrot,self.silver,self.concrete,self.sun_flower,self.green_sea],2)
        self.color1 , self.color2 = color

    def design_food1(self):
        text = self.food_font.render(f'{self.generate_random_answer()}', True, self.color1)
        self.game_window.blit(text, (self.food_x1, self.food_y1))

    def design_food2(self):
        text = self.food_font.render(f'{self.generate_true_answer()}', True, self.color2)
        self.game_window.blit(text, (self.food_x2, self.food_y2))

    def display_score(self,score):
        font = pygame.font.SysFont(None, 15)
        text = font.render(f'{score}', True, self.blue)
        self.game_window.blit(text, [10, 10])

    def display_question(self):
        font = pygame.font.SysFont(None, 15)
        text = font.render(f'{self.generate_question_string()}', True, self.turquoise)
        self.game_window.blit(text, [self.window_width / 2, 10])
    
    def score_table_show(self):
        font_style = pygame.font.SysFont(None, 15)
        message = font_style.render(str(self.snake_length - 1), True, self.black)
        self.game_window.blit(message, [self.window_width / 2, self.window_height / 2])
        pygame.display.update()
        time.sleep(2) 

    def reset(self):
        self._init_windows()
        self.generate_question()
        self.choose_color()
        self.snake_list = []
        self.snake_length = 1
        self.snake_x = self.window_width / 2
        self.snake_y = self.window_height / 2
        self.snake_x_change = 0
        self.snake_y_change = 0
        self.food_x1 = round(random.randrange(0, self.window_width - self.snake_block) / 20.0) * 20.0
        self.food_y1 = round(random.randrange(0, self.window_height - self.snake_block) / 20.0) * 20.0
        self.food_x2 = round(random.randrange(0, self.window_width - self.snake_block) / 20.0) * 20.0
        self.food_y2 = round(random.randrange(0, self.window_height - self.snake_block) / 20.0) * 20.0

        observation = self.get_observation()
        return observation

    def step(self,action):
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
            reward = -10
            done = True

        if [self.snake_x, self.snake_y] in self.snake_list[:-1]:
            self.score_table_show()
            reward = -10
            done = True

        if self.snake_x == self.food_x1 and self.snake_y == self.food_y1:
            self.score_table_show()
            reward = -10
            done = True

        self.game_window.fill(self.white)
        self.design_food1()
        self.design_food2()
        snake_head = []
        snake_head.append(self.snake_x)
        snake_head.append(self.snake_y)
        self.snake_list.append(snake_head)
        if len(self.snake_list) > self.snake_length:
            del self.snake_list[0]

        self.design_snake(self.snake_block, self.snake_list)
        self.display_score(self.snake_length - 1)
        self.display_question()
        pygame.display.update()

        # if self.snake_x == self.food_x1 and self.snake_y == self.food_y1:
        #     self.food_x1 = round(random.randrange(0, self.window_width - self.snake_block) / 20.0) * 20.0
        #     self.food_y1 = round(random.randrange(0, self.window_height - self.snake_block) / 20.0) * 20.0
        #     self.snake_length += 1
        #     reward = 10

        if self.snake_x == self.food_x2 and self.snake_y == self.food_y2:
            self.generate_question()
            self.choose_color()
            self.food_x1 = round(random.randrange(0, self.window_width - self.snake_block) / 20.0) * 20.0
            self.food_y1 = round(random.randrange(0, self.window_height - self.snake_block) / 20.0) * 20.0
            self.food_x2 = round(random.randrange(0, self.window_width - self.snake_block) / 20.0) * 20.0
            self.food_y2 = round(random.randrange(0, self.window_height - self.snake_block) / 20.0) * 20.0
            self.snake_length += 1
            reward = 10

        observation = self.get_observation()
        return observation, reward, done, {}

    def get_observation(self):
        observation = pygame.surfarray.array3d(pygame.display.get_surface())
        observation = np.transpose(observation, axes=(1, 0, 2))
        return observation

    def render(self, mode=None):
        # 在屏幕上显示游戏状态
        self.game_window.fill(self.white)
        self.design_food1()
        self.design_food2()
        self.design_snake(self.snake_block, self.snake_list)
        self.display_score(self.snake_length - 1)
        self.display_question()
        pygame.display.update()
        self.clock.tick(self.snake_speed)
        
        if mode in ('human','h') :
            # 等待玩家操作
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_UP:
                        return 0 
                    elif event.key == pygame.K_DOWN:
                        return 1
                    elif event.key == pygame.K_LEFT:
                        return 2
                    elif event.key == pygame.K_RIGHT:
                        return 3

    def close(self):
        pygame.quit()
        quit()
    
    def run(self):
        action = env.render(mode='h')
        if action != None :
            print(action)
        return self.step(action)

if __name__ == "__main__":

    env = snake()
    observation = env.reset()
    done = False

    while not done:
        observation, reward, done, _ = env.run()
