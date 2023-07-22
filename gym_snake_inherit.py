import gym 
from gym import spaces
from gym_snake import snake  # 假设你的原始代码保存在snake.py中
import numpy as np

class SnakeEnv(gym.Env):

    def __init__(self):
        super(SnakeEnv, self).__init__()

        self.snake_game = snake()  # 创建原始snake类的实例

        # 定义动作空间和状态空间
        self.action_space = spaces.Discrete(4)  # 假设游戏有4个动作可选：上、下、左、右
        self.observation_space = spaces.Box(low=0, high=255,
                                             shape=(self.snake_game.window_height, self.snake_game.window_width, 3),
                                               dtype=np.uint8)  # 假设游戏状态是RGB图像，大小为(window_height, window_width)

    def reset(self):
        return self.snake_game.reset()

    def step(self):
        print(self.action)
        return self.snake_game.step()

    def render(self,mode=None):
        # 在屏幕上显示游戏状态，这里需要调用原始snake类的渲染方法
        self.snake_game.render(mode=mode)

    def close(self):
        self.snake_game.close()

    def run(self):
        self.render(mode='h')
        return self.step()
    
if __name__ == '__main__':

    env = SnakeEnv()
    observation = env.reset()
    done = False

    while not done:
        env.action = env.action_space.sample()  # sample.
        observation, reward, done, _ = env.step()
        # print(reward)
        # env.render()

