"""
Simple snake-online environment with only direction control.
Infinite-mode.
"""

import logging
import win32gui as gui
import autopy
import time
import numpy as np
import aigame
from aigame import spaces

logger = logging.getLogger(__name__)

class SnakeOnlineOnlyDirEnv(aigame.Env):
    """
    def __init__(self)
    def _step(self, action)
    def _reset(self)
    def _get_obs(self)
    def _get_reward(self)
    def _window_search(self, title)
    def _game_to_top(self)
    def _env_analyze(self)
    def _analysis_status(self, obs)
    def _suicide_restart(self)
    def _restart(self)
    def _suicide(self)
    def _ctl_rst(self)
    def move(self, dx, dy)
    """

    NEW_GAME = 0
    IN_GAME = 1
    SCORE = 2
    RE_GAME = 3
    SUICIDE_SPEEDUP_INTERVAL = 20

    def __init__(self):
        """
        action_space contains 3 discrete action spaces:
            1) Directions: Discrete 121    - NOOP[0], Angle[1], ... Angle[120], 2*pi*angle/120
            2) Accelerate: Discrete 2      - NOOP[0], Accelerate[1]
            3) Shield:     Discrete 2      - NOOP[0], Shield[1]

        @TODO define the observasion space
        observasion_space contains 3 discrete observasion spaces:
            1) HasShield:  Discrete 2      - 
        """
        self.action_space = spaces.MultiDiscrete([ [0, 121], [0, 1], [0, 1] ])
        self.observation_space = None
        self._snakeWindow = None
        self._last_obs = {}
        self._cur_obs = {}
        self._reset()

    def _step(self, action):
        direction, accelerate, shield = action
        angle = 2 * np.pi * direction / 120
        dx = np.int(np.round(self.radius * np.cos(angle)))
        dy = np.int(np.round(self.radius * np.sin(angle)))
        self._ctl_dir(dx, dy)
        if shield == 1:
            self._shield()
        if accelerate == 1:
            self._accelerate()
        return self._get_obs(), self._get_reward(), self._cur_obs["status"] == self.IN_GAME, {}

    def _reset(self):
        self._game_to_top()
        self._env_analyze()
        self._suicide_restart()
        self._ctl_dir_rst()
        logger.info("reset the game.")
        return self._get_obs()

    # @TODO analyze current game status with ImageRecognition.
    def _get_obs(self):
        """
        Get the current observation of the GAME.
        """
        # Step1. take a snapeshot.
        # Step2. analyze scores, maybe also who kill who, left-top map(boss pos), score list.
        obs = {"status":self.RE_GAME, "screen":None,
               "shield":True, "score":10, "team":10, "rank":3,
               "bosslist":[], "teamlist":[]}
        if self._cur_obs:
            self._last_obs = self._cur_obs
        self._cur_obs = obs
        return obs

    # @TODO analysis score reward.
    def _get_reward(self):
        """
        There are lots of reward formats:
            1). self score change
            2). team score change
            3). self kill-snake change
            4). team rank change
            5). other teams score change
        """
        assert(self._cur_obs)
        if self._last_obs:
            return self._cur_obs["score"] - self._last_obs["score"]
        else:
            return self._cur_obs["score"]

    def _window_search(self, title):
        def _window_search_(hwnd, title):
            """
            if gui.IsWindow(hwnd) and gui.IsWindowEnabled(hwnd) and \
              gui.IsWindowVisible(hwnd) and title in gui.GetWindowText(hwnd):
            """
            if title in gui.GetWindowText(hwnd):
                logger.info("GetHandle %d for window %s."%(hwnd, gui.GetWindowText(hwnd)))
                self._snakeWindow = hwnd
        gui.EnumWindows(_window_search_, title)

    def _game_to_top(self):
        self._snakeWindow = None
        windowTitle = "Bluestacks"
        self._window_search(windowTitle)
        if self._snakeWindow:
            logger.info("Bring window %s to top."%(windowTitle))
            gui.BringWindowToTop(self._snakeWindow)
            gui.SetForegroundWindow(self._snakeWindow)
            time.sleep(2)
        else:
            raise EnvironmentError("Game Window Not Found.")

    # @TODO auto-detect these information.
    def _env_analyze(self):
        self.dirCenter = (251, 565)
        self.spdCenter = (1124, 567)
        self.rstCenter = (816, 468)
        self.sldCenter = (1114, 565)
        self.dirX = self.dirCenter[0]
        self.dirY = self.dirCenter[1]
        self.spdX = self.spdCenter[0]
        self.spdY = self.spdCenter[1]
        self.rstX = self.rstCenter[0]
        self.rstY = self.rstCenter[1]
        self.sldX = self.sldCenter[0]
        self.sldY = self.sldCenter[1]
        self.radius = 50
        self._snakeWindowRect = gui.GetWindowRect(self._snakeWindow)

    def _analysis_status(self, obs):
        return obs.get("status", self.IN_GAME)

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
        logger.info("restart the game.")
        self._left_click(self.rstX, self.rstY)

    # @TODO how to commit a suicide quickly?
    def _suicide(self):
        logger.info("commit a suicide.")
        autopy.mouse.toggle(False, autopy.mouse.LEFT_BUTTON)
        autopy.mouse.move(self.spdX, self.spdY)
        autopy.mouse.toggle(True, autopy.mouse.LEFT_BUTTON)
        time.sleep(self.SUICIDE_SPEEDUP_INTERVAL)
        autopy.mouse.toggle(False, autopy.mouse.LEFT_BUTTON)

    def _ctl_dir_rst(self):
        logger.info("direction control reset.")
        self._left_click(self.dirX, self.dirY)

    def _ctl_dir(self, dx, dy):
        logger.info("control dir.")
        autopy.mouse.toggle(False, autopy.mouse.LEFT_BUTTON)
        autopy.mouse.move(self.dirX, self.dirY)
        autopy.mouse.toggle(True, autopy.mouse.LEFT_BUTTON)
        autopy.mouse.smooth_move(self.dirX + dx, self.dirY + dy)
        autopy.mouse.toggle(False, autopy.mouse.LEFT_BUTTON)

    def _shield(self):
        logger.info("shield.")
        self._left_click(self.sldX, self.sldY)

    def _accelerate(self):
        logger.info("accelerate.")
        self._left_click(self.spdX, self.spdY)        

    def _left_click(self, x, y):
        autopy.mouse.toggle(False, autopy.mouse.LEFT_BUTTON)
        autopy.mouse.move(x, y)
        autopy.mouse.click(autopy.mouse.LEFT_BUTTON)
