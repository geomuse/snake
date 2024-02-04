import pygame
import sys

pygame.init()

# 设置窗口
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Input Example")

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # 检测键盘按下事件
            if event.key == pygame.K_LEFT:
                print("Left arrow key pressed")
            elif event.key == pygame.K_RIGHT:
                print("Right arrow key pressed")
            elif event.key == pygame.K_UP:
                print("Up arrow key pressed")
            elif event.key == pygame.K_DOWN:
                print("Down arrow key pressed")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 检测鼠标按下事件
            if event.button == 1:
                print("Left mouse button pressed")
            elif event.button == 3:
                print("Right mouse button pressed")

    # 渲染更新
    screen.fill((255, 255, 255))
    pygame.display.flip()

# 退出程序
pygame.quit()
sys.exit()
