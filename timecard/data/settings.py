"""Settings [Timecard]
Author(s): Jason C. McDonald

Manages access, storage, and file read/write for application settings.
"""

import functools
import logging
import os
from pathlib import Path


def settings_getter(func):
    """Ensure settings are loaded appropriately."""
    @functools.wraps(func)
    def wrapper(*args, **vargs):
        Settings.load()
        return func(*args, **vargs)
    return wrapper


def settings_setter(func):
    """Ensure settings are loaded from and saved to file appropriately."""
    @functools.wraps(func)
    def wrapper(*args, **vargs):
        Settings.load()
        r = func(*args, **vargs)
        Settings.save()
        return r
    return wrapper


class Settings:
    _settings = None
    _settings_path = Path(Path.home(), ".timecardrc")

    @classmethod
    def load(cls, force=False):
        """Load the settings from either file (if it exists) or default."""

        # If we've already loaded, don't reload unless forced to.
        if not force and cls._settings is not None:
            return

        if cls._settings_path.exists():
            cls.load_from_file()
        else:
            cls.load_from_default()

    @classmethod
    def load_from_file(cls):
        """Load the settings from file.
        You probably shouldn't use this directly; use Settings.load() instead.
        """
        cls._settings = dict()

        logging.debug(f"Loading settings from {str(cls._settings_path)}")

        with cls._settings_path.open('r') as file:
            for lineno, line in enumerate(file, start=1):
                try:
                    k, v = (s.strip() for s in line.split(sep='=', maxsplit=2))
                except ValueError:
                    logging.warning(f"Invalid entry in .timecardrc:{lineno}\n"
                                    f"  {line}")
                else:
                    cls._settings[k] = v

    @classmethod
    def load_from_default(cls):
        """Load the settings from default.
        You probably shouldn't use this directly; use Settings.load() instead.
        """
        cls._settings = dict()

        cls._settings['datefmt'] = cls.get_datefmt()
        cls._settings['decdur'] = str(cls.get_decdur())
        cls._settings['logdir'] = cls.get_logdir_str()
        cls._settings['logname'] = cls.get_logname()
        cls._settings['persist'] = str(cls.get_persist())

    @classmethod
    def save(cls):
        """Save the log to file."""
        with cls._settings_path.open('w') as file:
            for key, value in cls._settings.items():
                file.write(f"{key}={value}\n")

    @classmethod
    @settings_getter
    def get_logdir_str(cls):
        """Get the log directory path as a string."""
        try:
            logdir = cls._settings['logdir']
            return os.path.normpath(logdir)
        except KeyError:
            return str(Path(Path.home(), ".timecard"))

    @classmethod
    @settings_getter
    def get_logdir(cls):
        """Get the log directory path."""
        logdir = cls.get_logdir_str()
        return Path(*(logdir.split(os.pathsep)))

    @classmethod
    @settings_setter
    def set_logdir(cls, logdir):
        """Set the log path."""
        cls._settings['logdir'] = logdir

    @classmethod
    @settings_getter
    def get_logname(cls):
        """Get the log filename."""
        try:
            return cls._settings['logname']
        except KeyError:
            return "time.log"

    @classmethod
    @settings_setter
    def set_logname(cls, logname):
        """Set the log path."""
        cls._settings['logname'] = logname

    @classmethod
    @settings_getter
    def get_logpath(cls):
        """Get the full log path."""
        return cls.get_logdir().joinpath(cls.get_logname())

    @classmethod
    @settings_getter
    def get_persist(cls):
        """Returns whether closing the window should hide it or quit."""
        try:
            return cls._settings['persist'] != 'False'
        except KeyError:
            return True

    @classmethod
    @settings_setter
    def set_persist(cls, persist):
        """Sets persistence."""
        cls._settings['persist'] = str(persist)

    @classmethod
    @settings_getter
    def get_datefmt(cls):
        """Returns timestamp format (should be in 1989 C standard)."""
        try:
            return cls._settings['datefmt']
        except KeyError:
            return "%Y-%m-%d %H:%M:%S"

    @classmethod
    @settings_setter
    def set_datefmt(cls, datefmt):
        cls._settings['datefmt'] = datefmt

    @classmethod
    @settings_getter
    def get_decdur(cls):
        """Returns whether duration should be displayed as decimal
        or HH:MM;SS.
        """
        try:
            return cls._settings['decdur'] != 'False'
        except KeyError:
            return False

    @classmethod
    @settings_setter
    def set_decdur(cls, decdur):
        """Sets whether duration should be displayed as decimal."""
        cls._settings['decdur'] = str(decdur)
