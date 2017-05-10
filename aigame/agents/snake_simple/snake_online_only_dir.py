"""
Simple snake-online environment with only direction control.
Infinite-mode.
"""

import logging
import win32gui as gui
import autopy
import time
import math
import random
import aigame
from aigame import spaces

logger = logging.getLogger(__name__)

class SnakeOnlineOnlyDirEnv(aigame.Env):
    NEW_GAME = 0
    IN_GAME = 1
    SCORE = 2
    RE_GAME = 3
    def __init__(self):
        self._snakeWindow = None
        self._status = self.RE_GAME
        self._reset()

    def _step(self, action):
        if action:
                reward = 1
        else:
                reward = 0
        done = True
        return self._get_obs(), reward, done, {}

    # @TODO analyze current game status with ImageRecognition.
    def _get_obs(self):
        '''
        Get the current observation of the GAME.
        '''
        return 0

    def _reset(self):
        self._game_to_top()
        self._init()
        self._suicide_restart()
        return self._get_obs()

    def window_search(self, title):
        def _window_search(hwnd, title):
            '''
            if gui.IsWindow(hwnd) and gui.IsWindowEnabled(hwnd) and \
              gui.IsWindowVisible(hwnd) and title in gui.GetWindowText(hwnd):
            '''
            if title in gui.GetWindowText(hwnd):
                logger.info("GetHandle %d for window %s."%(hwnd, gui.GetWindowText(hwnd)))
                self._snakeWindow = hwnd
        gui.EnumWindows(_window_search, title)

    def _game_to_top(self):
        self._snakeWindow = None
        windowTitle = "Bluestacks"
        self.window_search(windowTitle)
        if self._snakeWindow:
            logger.info("Bring window %s to top."%(windowTitle))
            gui.BringWindowToTop(self._snakeWindow)
            gui.SetForegroundWindow(self._snakeWindow)

    # @TODO auto-detect these information.
    def _init(self):
        self.dirCenter = (251, 565)
        self.spdCenter = (1124, 567)
        self.rstCenter = (816, 468)
        self.dirX = self.dirCenter[0]
        self.dirY = self.dirCenter[1]
        self.spdX = self.spdCenter[0]
        self.spdY = self.spdCenter[1]
        self.rstX = self.rstCenter[0]
        self.rstY = self.rstCenter[1]

    def _analysis_status(self, obs):
        return self.RE_GAME

    def _suicide_restart(self):
        """
        Commit a suicide first if game not finished.
        And then restart it.
        """
        obs = self._get_obs()
        if self._analysis_status(obs) != self.RE_GAME:
            self._suicide()
        self._restart()

    def _restart(self):
        """
        Restart the game.
        """
        autopy.mouse.toggle(False, autopy.mouse.LEFT_BUTTON)
        autopy.mouse.move(self.rstX, self.rstY)
        autopy.mouse.click(autopy.mouse.LEFT_BUTTON)

    # @TODO how to commit a suicide quickly?
    def _suicide(self):
        autopy.mouse.toggle(False, autopy.mouse.LEFT_BUTTON)
        autopy.mouse.move(self.spdX, self.spdY)
        autopy.mouse.toggle(True, autopy.mouse.LEFT_BUTTON)
        time.sleep(20)
        autopy.mouse.toggle(False, autopy.mouse.LEFT_BUTTON)

    def _ctl_rst(self):
        autopy.mouse.toggle(False, autopy.mouse.LEFT_BUTTON)
        autopy.mouse.move(self.dirX, self.dirY)

    def move(self, dx, dy):
        autopy.mouse.toggle(True, autopy.mouse.LEFT_BUTTON)
        autopy.mouse.smooth_move(self.dirX + dx, self.dirY + dy)
        #autopy.mouse.toggle(False, autopy.mouse.LEFT_BUTTON)

# Step1. find window for snake and set it top.
# Step2. control the snake
