"""App [Timecard]
Version: 2.0
Author(s): Jason C. McDonald
"""

import logging

from timecard import interface
from timecard.interface import App

logging.basicConfig(level=logging.DEBUG)


def startUI():
    App.build()
    interface.build()

    return App.run()
