from datetime import datetime
import functools
import logging
import os

from timecard.data.settings import Settings


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


class LogEntry:

    def __init__(self, timestamp=None, duration=(0, 0, 0), notes=""):
        self.timestamp = timestamp
        self.duration = duration
        self.notes = notes

    def set_timestamp(self, year, month, day, hour, minute, second):
        self.timestamp = datetime(year, month, day, hour, minute, second)

    def set_timestamp_from_string(self, timestamp_str):
        try:
            ts = [int(n) for n in timestamp_str.split('-')]
            self.set_timestamp(*ts)
        except (TypeError, ValueError):
            return False
        return True

    def set_duration(self, hours, minutes, seconds):
        self.duration = (hours, minutes, seconds)

    def set_duration_from_string(self, duration_str):
        try:
            duration = [int(n) for n in duration_str.split(':')]
            self.set_duration(*duration)
        except (TypeError, ValueError):
            return False
        return True

    def timestamp_as_string(self):
        return (f"{self.timestamp.year}-{self.timestamp.month}-"
                f"{self.timestamp.day}-{self.timestamp.hour}-"
                f"{self.timestamp.minute}-{self.timestamp.second}")

    def timestamp_as_format(self, format):
        return self.timestamp.strftime(format)

    def duration_as_string(self):
        return (f"{self.duration[0]:02}:"
                f"{self.duration[1]:02}:"
                f"{self.duration[2]:02}")

    def set_notes(self, notes):
        self.notes = notes


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
                    entry_raw = line.strip().split('|', 3)

                    # If we don't get three fields,
                    # log a warning and skip the entry.
                    if len(entry_raw) != 3:
                        logging.warning(f"Invalid entry in {path}:{lineno}\n"
                                        f"  {line}")
                        continue

                    # Add the entry to the log.
                    entry = LogEntry()
                    entry.set_timestamp_from_string(entry_raw[0])
                    entry.set_duration_from_string(entry_raw[1])
                    entry.set_notes(entry_raw[2])

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
                file.write((f"{entry.timestamp_as_string()}|"
                            f"{entry.duration_as_string()}|"
                            f"{entry.notes}\n"))

    @classmethod
    @timelog_getter
    def retrieve_log(cls):
        """Returns the log, loading it from file if necessary."""
        return cls._log

    @classmethod
    @timelog_getter
    def retrieve_from_log(cls, index):
        """Returns an entry in the log, loading from file if necessary."""
        try:
            return cls._log[index]
        except IndexError:
            logging.warning("Cannot access entry at invalid log index.")
            return None

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
        entry = LogEntry()
        entry.set_timestamp_from_string(timestamp)
        entry.set_duration(hours, minutes, seconds)
        entry.set_notes(notes)

        cls._log.append(entry)

    @classmethod
    @timelog_setter
    def edit_in_log(cls, index, timestamp, hours, minutes, seconds, notes):
        """Edit an entry in the log.
        This relies on the indices in LogView and TimeLog being the same.
        FIXME: This assumption fails when log is sorted!

        index -- the index of the item to edit
        """
        entry = LogEntry()
        entry.set_timestamp_from_string(timestamp)
        entry.set_duration(hours, minutes, seconds)
        entry.set_notes(notes)
        try:
            cls._log[index] = entry
        except IndexError:
            logging.warning("Cannot edit entry at invalid log index.")

    @classmethod
    @timelog_setter
    def remove_from_log(cls, index):
        """Remove an entry from the log.
        This relies on the indices in LogView and TimeLog being the same.
        FIXME: This assumption fails when log is sorted!

        index -- the index of the item to remove
        """
        try:
            del cls._log[index]
        except IndexError:
            logging.warning("Cannot delete entry at invalid log index.")
