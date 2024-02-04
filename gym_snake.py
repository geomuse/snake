import gym 
from gym import spaces
import numpy as np
import pickle

import os , sys
current_dir = os.path.dirname(os.path.abspath(__file__))
path = '/home/geo/Downloads/geo'
sys.path.append(path)

from notification_bot.loguru_notification import loguru_notf
from game_bot.snake.pygame_snake import snake
logger = loguru_notf(current_dir)
logger.add('snake')

class SnakeEnv(gym.Env):

    def __init__(self):
        super(SnakeEnv, self).__init__()
        self.snake_game = snake()
        # 定义动作空间和状态空间
        self.action_space = spaces.Discrete(4)  # 假设游戏有4个动作可选：上、下、左、右
        self.observation_space = spaces.Box(low=0, high=255,
                                             shape=(self.snake_game.window_height, self.snake_game.window_width, 3),
                                               dtype=np.uint8)  # 假设游戏状态是RGB图像，大小为(window_height, window_width)

    def reset(self):
        return self.snake_game.reset()

    def step(self,action):
        return self.snake_game.step(action)

    def render(self,mode=None):
        # 在屏幕上显示游戏状态，这里需要调用原始snake类的渲染方法
        self.snake_game.render(mode=mode)

    def close(self):
        self.snake_game.close()

    def run(self):
        action = self.snake_game.render(mode='h')
        if action != None :
            print(action)
        return self.step(action)
    
    def random(self):
        action = self.action_space.sample()  # sample.
        if action != None :
            print(action)
        return self.step(action)
    
    def rl_run(self,observation):
        with open(f'{current_dir}/data/q_table.pkl', 'rb') as f:
            q_table = pickle.load(f)
        
        action = np.argmax(q_table[observation, :])
        return env.step(action)

    def framework(self,mode=None):
        observation = self.reset()
        done = False

        if mode in ('sample','human' , 'h' ,'rl'):
            match mode :
                case 'sample':
                    while not done:
                        observation, reward, done, _ = self.random()
                case 'human' | 'h': 
                    while not done:
                        observation, reward, done, _ = self.run()
                case 'rl' :
                    while not done:
                        next_observation , _ , done , _ = self.rl_run(observation)
                        self.render()
                        observation = next_observation

if __name__ == '__main__':

    env = SnakeEnv()
    env.framework(mode='h')
        


