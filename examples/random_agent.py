import logging
import sys

from aigame.agents import snake_simple
from aigame.envs import snake_online

if __name__ == '__main__':
    env = snake_online.SnakeOnlineOnlyDirEnv()
    agent = snake_simple.RandomSnakeAgent(env)

    episode_count = 2
    reward = 0
    done = False

    for i in range(episode_count):
        loop = 0
        ob = env.reset()
        while True:
            action = agent.act(ob, reward, done)
            ob, reward, done, _ = env.step(action)
            loop += 1
            if done or loop >= 200:
                break

    # Close the env and write monitor result info to disk
    env.close()

    logger.info("Successfully ran RandomAgent.")
