import functools
import logging
import os
from . import Settings


def timelog_getter(func):
    """Ensure settings are loaded appropriately."""
    @functools.wraps(func)
    def wrapper(*args, **vargs):
        # Ensure log is loaded from file
        TimeLog.load()
        return func(*args, **vargs)
    return wrapper


def timelog_setter(func):
    """Ensure settings are loaded from and saved to file appropriately."""
    @functools.wraps(func)
    def wrapper(*args, **vargs):
        # Ensure log is loaded from file
        TimeLog.load()
        r = func(*args, **vargs)
        # Immediately write the log to file
        TimeLog.save()
        return r
    return wrapper


class TimeLog:
    _log = None

    @classmethod
    def load(cls, /, force=False):
        """Load the time log from file."""

        # If we've already loaded, don't reload unless forced to.
        if not force and cls._log is not None:
            return

        # Retrieve the path from settings
        path = Settings.get_logpath()

        # Initialize an empty log.
        cls._log = []
        # Attempt to open and parse the file.
        try:
            with path.open('r') as file:
                # Process each line in the log file
                for lineno, line in enumerate(file, start=1):
                    # Each entry consists of three fields, separated by pipes
                    entry = line.strip().split('|', 3)

                    # If we don't get three fields,
                    # log a warning and skip the entry.
                    if len(entry) != 3:
                        logging.warning(f"Invalid entry in {path}:{lineno}\n"
                                        f"  {line}")
                        continue

                    # Add the entry to the log.
                    cls._log.append(entry)
        # If no log file exists, move forward with the empty log (default).
        except FileNotFoundError:
            pass

    @classmethod
    def save(cls):
        """Save the time log to file."""

        # Retrieve the save directory from settings
        logdir = Settings.get_logdir()
        # Create the save directory if necessary
        if not logdir.exists():
            os.makedirs(logdir)

        # Retrieve the full save path from settings
        logpath = Settings.get_logpath()
        # Write the log out to the file.
        with logpath.open('w') as file:
            for entry in cls._log:
                file.write(f'{entry[0]}|{entry[1]}|{entry[2]}\n')

    @classmethod
    @timelog_getter
    def retrieve_log(cls):
        """Returns the log, loading it from file if necessary."""
        return cls._log

    @classmethod
    @timelog_setter
    def add_to_log(cls, timestamp, hours, minutes, seconds, notes):
        """Add an entry to the log.

        timestamp -- the timestamp as a string
        hours -- the number of elapsed hours
        minutes -- the number of elapsed minutes
        seconds -- the number of elapsed seconds
        notes -- the activity description string for the entry
        """
        # Add the entry directly to the log.
        cls._log.append((
            f"{timestamp}",
            f"{hours:02}:{minutes:02}:{seconds:02}",
            f"{notes}"
        ))
