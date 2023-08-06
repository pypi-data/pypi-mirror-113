import warnings

from authorship import (
    __author__,
    __copyright__,
    __license__,
    __title__,
    __url__,
    __version__,
    default_app_config,
)


__all__ = [
    "__author__",
    "__copyright__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "default_app_config",
]


warnings.warn(
    "thecut.authorship has been renamed authorship. "
    "This alias will be removed in the future.",
    DeprecationWarning,
)
