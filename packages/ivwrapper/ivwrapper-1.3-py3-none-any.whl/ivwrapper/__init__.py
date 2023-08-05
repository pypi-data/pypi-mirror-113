from .ivwrapper import *

__title__ = "ivwrapper"
__summary__ = "Asynchroniczny wrapper dla api ivall'a."
__uri__ = "https://github.com/Nohet/ivwrapper"
__version__ = "1.3"
__author__ = "Nohet"
__email__ = "igorczupryniak503@gmail.com"
__license__ = "MIT License"
__copyright__ = f"Copyright 2021 {__author__}"


async def get_version():
    return __version__
