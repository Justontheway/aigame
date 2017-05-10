"""
Simple Snake with only direction control.
"""

import logging
import aigame
import random
from aigame import spaces

logger = logging.getLogger(__name__)

class SimpleSnakeAgent(aigame.Agent):
    def __init__(self, env):
        self.action_space = env.action_space
        self.observation_space = env.observation_space

    def _act(self, observation, reward, done):
        """
        Return next action based on the last observation and
        reward and status.
        """
        return self.action_space.sample()

class RandomSnakeAgent(aigame.Agent):
    def __init__(self, env):
        self.action_space = env.action_space
        self.observation_space = env.observation_space

    def _act(self, observation, reward, done):
        """
        Return next action based on the last observation and
        reward and status.
        """
        action = self.action_space.sample()
        logger.info("take a action (%d, %d, %d)"%(action[0], action[1], action[2]))
        return action