"""
idotmatrix.

Library to configure any iDotMatrix compatible 16x16 or 32x32 pixel display without the chinese iDotMatrix android / iOS app.
"""

from .version import __version__
from idotmatrix import logger
from idotmatrix.connectionManager import ConnectionManager
from .modules.clock import Clock
from .modules.chronograph import Chronograph
from .modules.common import Common
from .modules.countdown import Countdown
from .modules.eco import Eco
from .modules.fullscreenColor import FullscreenColor
from .modules.gif import Gif
from .modules.graffiti import Graffiti
from .modules.image import Image
from .modules.musicSync import MusicSync
from .modules.scoreboard import Scoreboard
from .modules.system import System
from .modules.text import Text
from .modules.effect import Effect


__author__ = "Kalle Minkner, Jon-Mailes Graeffe"
__credits__ = (
    "everyone who thankfully helped with the reverse-engineering. You are awesome!"
)
__all__ = [
    "ConnectionManager",
    "Clock",
    "Chronograph",
    "Common",
    "Countdown",
    "Eco",
    "FullscreenColor",
    "Gif",
    "Graffiti",
    "Image",
    "MusicSync",
    "Scoreboard",
    "System",
    "Text",
    "Effect",
]
