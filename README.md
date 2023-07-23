# 贪吃蛇.

## 游戏基本框架.

`reset()`, `step()`, `render()`, 和 `close()`

```
reset()函数用于初始化游戏环境，并返回初始状态；

step()函数用于执行动作并返回新的状态、奖励和done标志；

render()函数用于在屏幕上显示游戏状态（在训练中通常不需要使用）；

close()函数用于关闭游戏窗口。

这些函数配合gym库的其他函数可以用来进行强化学习的训练和测试。
```

## 状态空间的维度.

```
状态空间的维度为(600, 800, 3)，这是一个三维数组。然而，对于DQN模型(dnn)，我们通常期望状态空间是一个一维的向量或者多维的矩阵，并不适合处理三维数组。

为了让状态空间符合DQN模型的要求，你需要将三维数组转换为一个合适的形状。这通常涉及到以下几个步骤：

    预处理和归一化：根据环境的特性，你可能需要对原始的状态空间进行预处理和归一化，使其范围在一个合适的值内，通常是[-1, 1]或[0, 1]之间。

    降维或变换：如果状态空间的维度太高，可以考虑采用降维技术，例如使用主成分分析（PCA）或卷积神经网络（CNN）提取特征。

    调整维度：将状态空间调整为DQN模型期望的形状，通常是一个向量或矩阵。

也可以换cnn模型进行训练.
```

## reset.

初始化到底要3维还是1维?

```
看模型.
```

## 在colab训练资料.

上传文件 `gym_snake.py` , `gym_snake_inherit.py` 到 colab .

```
!python --version
```

```
import gym
import numpy as np
import random
import tensorflow as tf
import time
```

```
from gym_snake_inherit import SnakeEnv
```

```
env = SnakeEnv()
observation = env.reset()
done = False

while not done:
    observation, reward, done, _ = env.sample()
```

## `snake.py`

简单的介面.

## `advance_snake.py`

极简风格的计分.

## `snake_for_reinforcement_learning.py`

承接 `advance_snake.py` 的设计风格用强化学习训练蛇并且跟你一起抢果实.
