import pygame
import time
import random
from dataclasses import dataclass
pygame.init()

@dataclass
class snake:
    
    # 游戏窗口大小和速度设置
    window_width = 800
    window_height = 600
    snake_block = 10
    snake_speed = 15

    # 定义颜色
    black = (0, 0, 0)
    white = (255, 255, 255)
    purple = (155, 89, 182)
    green = (46, 204, 113)
    blue = (52, 152, 219)

    def _init_windows(self):
        # 创建游戏窗口
        self.game_window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('贪吃蛇游戏')
        
    # 画蛇的函数
    def design_snake(self,snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.game_window, self.green, [x[0], x[1], snake_block, snake_block])

    # 显示得分
    def display_score(self,score):
        font = pygame.font.SysFont(None, 15)
        text = font.render(str(score), True, self.blue)
        self.game_window.blit(text, [10, 10])

    # 主游戏循环
    def game_loop(self):
        self._init_windows()
    
        game_over = False

        snake_list = []
        snake_length = 1

        snake_x = self.window_width / 2
        snake_y = self.window_height / 2

        snake_x_change = 0
        snake_y_change = 0

        food_x = round(random.randrange(0, self.window_width - self.snake_block) / 20.0) * 20.0
        food_y = round(random.randrange(0, self.window_height - self.snake_block) / 20.0) * 20.0

        clock = pygame.time.Clock()

        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        snake_x_change = -self.snake_block
                        snake_y_change = 0
                    elif event.key == pygame.K_RIGHT:
                        snake_x_change = self.snake_block
                        snake_y_change = 0
                    elif event.key == pygame.K_UP:
                        snake_y_change = -self.snake_block
                        snake_x_change = 0
                    elif event.key == pygame.K_DOWN:
                        snake_y_change = self.snake_block
                        snake_x_change = 0

            if snake_x >= self.window_width or snake_x < 0 or snake_y >= self.window_height or snake_y < 0:
                game_over = True

            snake_x += snake_x_change
            snake_y += snake_y_change

            self.game_window.fill(self.white)
            pygame.draw.rect(self.game_window, self.purple, [food_x, food_y, self.snake_block, self.snake_block])
            snake_head = []
            snake_head.append(snake_x)
            snake_head.append(snake_y)
            snake_list.append(snake_head)
            if len(snake_list) > snake_length:
                del snake_list[0]

            for x in snake_list[:-1]:
                if x == snake_head:
                    game_over = True

            self.design_snake(self.snake_block, snake_list)
            self.display_score(snake_length - 1)
            pygame.display.update()

            if snake_x == food_x and snake_y == food_y:
                food_x = round(random.randrange(0, self.window_width - self.snake_block) / 20.0) * 20.0
                food_y = round(random.randrange(0, self.window_height - self.snake_block) / 20.0) * 20.0
                snake_length += 1

            clock.tick(self.snake_speed)

        # 显示游戏结束信息
        font_style = pygame.font.SysFont(None, 15)
        message = font_style.render(str(snake_length - 1), True, self.black)
        self.game_window.blit(message, [self.window_width / 2, self.window_height / 2])
        pygame.display.update()
        time.sleep(2)  # 等待2秒后退出游戏

        pygame.quit()
        quit()

if __name__ == '__main__':
    g = snake()
    g.game_loop()
