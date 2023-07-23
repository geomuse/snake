from gym_snake_inherit import SnakeEnv  # 假设上面的代码保存在snake_env.py中

if __name__ == '__main__':

    env = SnakeEnv()
    observation = env.reset()
    done = False

    while not done:
        observation, reward, done, _ = env.sample()