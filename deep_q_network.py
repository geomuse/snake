import gym
import numpy as np
import random , time
import tensorflow as tf
from dataclasses import dataclass
import pickle

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten
from tensorflow.keras.optimizers import Adam

import matplotlib.pyplot as pt
from matplotlib import style
style.use('ggplot')
from gym_snake_inherit import SnakeEnv

# 定义DQN智能体类
class DQNAgent:
    def __init__(self):
        # self.model = model  # 使用上面定义的CNN模型作为DQN的近似函数
        self.memory = []  # 经验回放缓冲区
        self.gamma = 0.95  # 折扣因子，用于计算累积奖励
        self.epsilon = 1.0  # 探索率，初始时完全探索
        self.epsilon_decay = 0.995  # 探索率衰减率
        self.epsilon_min = 0.01  # 最小探索率

    def create_model(self):
        # 创建DQN模型
        model = Sequential()
        model.add(Conv2D(16, kernel_size=(3, 3), activation='relu', input_shape=state_shape))
        model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
        model.add(Flatten())
        model.add(Dense(64, activation='relu'))
        model.add(Dense(env.action_space.n, activation='linear'))  # 输出层，动作空间大小

        model.compile(loss='mse', optimizer=Adam(learning_rate=0.001))
        self.model = model

    # 选择动作
    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(env.action_space.n)
        else:
            return np.argmax(self.model.predict(state)[0])

    # 记录经验并进行经验回放
    def remember_and_train(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        if len(self.memory) > 32:  # 经验回放缓冲区大小
            batch = random.sample(self.memory, 32)  # 随机抽样一个batch的经验进行训练
            self.replay(batch)

    # 使用经验回放训练模型
    def replay(self, batch):
        for state, action, reward, next_state, done in batch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

if __name__ == '__main__':

    env = SnakeEnv()

    state_shape = env.observation_space.shape

    # 初始化DQN智能体
    agent = DQNAgent()
    agent.model = agent.create_model()

    # 训练DQN
    num_episodes = 1000
    for episode in range(num_episodes):
        state = env.reset()
        state = state.reshape((1,) + state_shape)  # 添加一维batch维度
        done = False
        time = 0

        while not done:
            action = agent.choose_action(state)
            next_state, reward, done, _ = env.step(action)
            next_state = next_state.reshape((1,) + state_shape)  # 添加一维batch维度
            agent.remember_and_train(state, action, reward, next_state, done)
            state = next_state
            time += 1

        print("Episode: {}, Score: {}".format(episode, time))
    
    ''' for colab
    from google.colab import files
    import pickle

    with open('q_table.pkl', 'wb') as f:
        pickle.dump(q_table, f)

    files.download('q_table.pkl')
    '''

    with open('mdoel.pkl', 'wb') as f:
        pickle.dump(agent.model, f)
    