"""
[Timecard]
Version: 2.0
Author(s): Jason C. McDonald
"""

import logging

from timecard import interface
from timecard.interface import App
from timecard.data import TimeLog, Settings

logging.basicConfig(level=logging.DEBUG)


def startUI():
    App.build()

    Settings.load()
    TimeLog.load_from_file()

    interface.build()

    Settings.save_to_file()

    return App.run()
