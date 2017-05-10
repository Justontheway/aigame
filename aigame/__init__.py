import distutils.version
import logging
import os
import sys

from aigame import error
from aigame.configuration import logger_setup, undo_logger_setup
from aigame.version import VERSION as __version__

logger = logging.getLogger(__name__)

# We automatically configure a logger with a simple stderr handler. If
# you'd rather customize logging yourself, run undo_logger_setup.
#
# (Note: this code runs before importing the rest of aigame, since we may
# print a warning at load time.)
#
# It's generally not best practice to configure the logger in a
# library. We choose to do so because, empirically, many of our users
# are unfamiliar with Python's logging configuration, and never find
# their way to enabling our logging. Users who are aware of how to
# configure Python's logging do have to accept a bit of incovenience
# (generally by caling `aigame.undo_logger_setup()`), but in exchange,
# the library becomes much more usable for the uninitiated.
#
# Aigame's design goal generally is to be simple and intuitive, and while
# the tradeoff is definitely not obvious in this case, we've come down
# on the side of auto-configuring the logger.

if not os.environ.get('GYM_NO_LOGGER_SETUP'):
    logger_setup()
del logger_setup


from aigame.core import Env, Space, Agent, Wrapper, ObservationWrapper, ActionWrapper, RewardWrapper

__all__ = ["Env", "Space", "Agent"]
