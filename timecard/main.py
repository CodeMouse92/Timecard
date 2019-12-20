"""
[Timecard]
Version: 2.0
Author(s): Jason C. McDonald
"""

import logging

from timecard import interface

logging.basicConfig(level=logging.DEBUG)


def startUI():
    return interface.run()
