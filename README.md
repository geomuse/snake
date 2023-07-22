# 贪吃蛇项目.

## `snake.py`

简单的介面.

## `advance_snake.py`

极简风格的计分.

## `snake_for_reinforcement_learning.py`

承接 `advance_snake.py` 的设计风格用强化学习训练蛇并且跟你一起抢果实.

# 做游戏基本框架.

`reset()`, `step()`, `render()`, 和 `close()`

```
reset()函数用于初始化游戏环境，并返回初始状态；

step()函数用于执行动作并返回新的状态、奖励和done标志；

render()函数用于在屏幕上显示游戏状态（在训练中通常不需要使用）；

close()函数用于关闭游戏窗口。

这些函数配合gym库的其他函数可以用来进行强化学习的训练和测试。
```

# 在colab训练资料.

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

