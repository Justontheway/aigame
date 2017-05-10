import sys

class Error(Exception):
    pass

# Local errors

class Unregistered(Error):
    """Raised when the user requests an item from the registry that does
    not actually exist.
    """
    pass

class UnregisteredEnv(Unregistered):
    """Raised when the user requests an env from the registry that does
    not actually exist.
    """
    pass

class UnregisteredBenchmark(Unregistered):
    """Raised when the user requests an env from the registry that does
    not actually exist.
    """
    pass

class DeprecatedEnv(Error):
    """Raised when the user requests an env from the registry with an
    older version number than the latest env with the same name.
    """
    pass

class UnseedableEnv(Error):
    """Raised when the user tries to seed an env that does not support
    seeding.
    """
    pass

class DependencyNotInstalled(Error):
    pass

class UnsupportedMode(Exception):
    """Raised when the user requests a rendering mode not supported by the
    environment.
    """
    pass

class ResetNeeded(Exception):
    """When the monitor is active, raised when the user tries to step an
    environment that's already done.
    """
    pass

class ResetNotAllowed(Exception):
    """When the monitor is active, raised when the user tries to step an
    environment that's not yet done.
    """
    pass

class InvalidAction(Exception):
    """Raised when the user performs an action not contained within the
    action space
    """
    pass

# Video errors

class VideoRecorderError(Error):
    pass

class InvalidFrame(Error):
    pass
