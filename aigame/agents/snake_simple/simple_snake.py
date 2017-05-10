"""
Simple Snake with only direction control.
"""

import aigame
import random
from aigame import spaces

class SimpleSnakeAgent(aigame.Agent):
    def __init__(self, env):
        self.action_space = env.action_space
        self.observation_space = env.observation_space

    def _act(self, observation, reward, done):
        """
        Return next action based on the last observation and
        reward and status.
        """
        raise self.action_space.sample()

class RandomSnakeAgent(aigame.Agent):
    def __init__(self, env):
        self.action_space = env.action_space
        self.observation_space = env.observation_space

    def _act(self, observation, reward, done):
        """
        Return next action based on the last observation and
        reward and status.
        """
        raise self.action_space.sample()