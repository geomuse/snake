import pygame
import random

pygame.init()

# 游戏窗口大小和速度设置
window_width = 800
window_height = 600
snake_block = 10
snake_speed = 15

# 定义颜色
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)

# 创建游戏窗口
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('贪吃蛇游戏')

# 画蛇的函数
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(game_window, green, [x[0], x[1], snake_block, snake_block])

# 主游戏循环
def game_loop():
    game_over = False
    game_close = False

    snake_list = []
    snake_length = 1

    snake_x = window_width / 2
    snake_y = window_height / 2

    snake_x_change = 0
    snake_y_change = 0

    food_x = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0

    clock = pygame.time.Clock()

    while not game_over:

        while game_close:
            game_window.fill(white)
            font_style = pygame.font.SysFont(None, 50)
            message = font_style.render("game over. Q:quit C:restart.", True, black)
            game_window.blit(message, [window_width / 4, window_height / 2])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake_x_change = -snake_block
                    snake_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake_x_change = snake_block
                    snake_y_change = 0
                elif event.key == pygame.K_UP:
                    snake_y_change = -snake_block
                    snake_x_change = 0
                elif event.key == pygame.K_DOWN:
                    snake_y_change = snake_block
                    snake_x_change = 0

        if snake_x >= window_width or snake_x < 0 or snake_y >= window_height or snake_y < 0:
            game_close = True

        snake_x += snake_x_change
        snake_y += snake_y_change

        game_window.fill(white)
        pygame.draw.rect(game_window, red, [food_x, food_y, snake_block, snake_block])
        snake_head = []
        snake_head.append(snake_x)
        snake_head.append(snake_y)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(snake_block, snake_list)
        pygame.display.update()

        if snake_x == food_x and snake_y == food_y:
            food_x = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0
            snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

if __name__ == '__main__':
    game_loop() 
