import sys
if sys.version_info.major > 2:
    from aigame.envs.snake_online.snake_online import SnakeOnlineEnv
else:
    from aigame.envs.snake_online.snake_online3 import SnakeOnlineEnv
del sys