"""App [Timecard]
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

    Settings.load_from_default()
    Settings.save_to_file()
    TimeLog.load_from_file()

    interface.build()

    TimeLog.write_to_file()

    TimeLog.write_to_file()

    return App.run()
