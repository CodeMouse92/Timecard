"""Time Log [Timecard]
Author(s): Jason C. McDonald

Manages access, storage, and file read/write for the time log.
Also contains the class representing a single time log entry.
"""

import functools
import logging
import os
from datetime import datetime

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

    @staticmethod
    def normalize_timestamp(timestamp):
        """Normalizes the timestamp, throwing away milliseconds and
        timezone data.

        timestamp -- the timestamp to normalize

        Returns the normalized timestamp.
        """
        return datetime(
            timestamp.year,
            timestamp.month,
            timestamp.day,
            timestamp.hour,
            timestamp.minute,
            timestamp.second,
        )

    def set_timestamp(self, timestamp):
        """Normalize and set the timestamp."""
        self.timestamp = LogEntry.normalize_timestamp(timestamp)

    def set_timestamp_from_string(self, timestamp_str):
        """Set the timestamp from dash-delimited string."""
        try:
            ts = [int(n) for n in timestamp_str.split("-")]
            self.timestamp = datetime(*ts)
        except (TypeError, ValueError):
            return False
        return True

    def set_duration(self, hours, minutes, seconds):
        """Set duration from tuple.

        hours -- the number of hours
        minutes -- the number of minutes
        seconds -- the number of seconds
        """
        self.duration = (hours, minutes, seconds)

    def set_duration_from_string(self, duration_str):
        """Set duration from colon-delimited string."""
        try:
            duration = [int(n) for n in duration_str.split(":")]
            self.set_duration(*duration)
        except (TypeError, ValueError):
            return False
        return True

    def timestamp_as_string(self):
        """Retrieve timestamp as dash-delimited string."""
        return (
            f"{self.timestamp.year}-{self.timestamp.month}-"
            f"{self.timestamp.day}-{self.timestamp.hour}-"
            f"{self.timestamp.minute}-{self.timestamp.second}"
        )

    def timestamp_as_format(self, format):
        """Retrieve timestamp according to given format string."""
        return self.timestamp.strftime(format)

    def duration_as_string(self, as_decimal=False):
        """Retrieve duration in format HH:MM:SS"""
        if as_decimal:
            decdur = self.duration[0] + (self.duration[1] / 60)
            return f"{decdur:.2f}"
        else:
            return (
                f"{self.duration[0]:02}:"
                f"{self.duration[1]:02}:"
                f"{self.duration[2]:02}"
            )

    def set_notes(self, notes):
        """Retrive note string."""
        self.notes = notes


class TimeLog:
    _log = None

    @staticmethod
    def increment_timestamp(timestamp):
        return datetime(
            timestamp.year,
            timestamp.month,
            timestamp.day,
            timestamp.hour,
            timestamp.minute,
            timestamp.second + 1,
        )

    @classmethod
    def load(cls, force=False):
        """Load the time log from file."""

        # If we've already loaded, don't reload unless forced to.
        if not force and cls._log is not None:
            return

        # Retrieve the path from settings
        path = Settings.get_logpath()

        logging.debug(f"Loading time log from {path}")

        # Initialize an empty log.
        cls._log = dict()
        # Attempt to open and parse the file.
        try:
            with path.open("r", encoding="utf-8") as file:
                # Process each line in the log file
                for lineno, line in enumerate(file, start=1):
                    # Each entry consists of three fields, separated by pipes
                    entry_raw = line.strip().split("|", 3)

                    # If we don't get three fields,
                    # log a warning and skip the entry.
                    if len(entry_raw) != 3:
                        logging.warning(
                            f"Invalid entry in {path}:{lineno}\n" f"  {line}"
                        )
                        continue

                    # Create a log entry from the data line.
                    entry = LogEntry()
                    entry.set_timestamp_from_string(entry_raw[0])
                    entry.set_duration_from_string(entry_raw[1])
                    entry.set_notes(entry_raw[2])

                    # Add entry to log, using timestamp as key.
                    cls._log[entry.timestamp] = entry

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
        with logpath.open("w", encoding="utf-8") as file:
            for entry in cls._log.values():
                file.write(
                    (
                        f"{entry.timestamp_as_string()}|"
                        f"{entry.duration_as_string()}|"
                        f"{entry.notes}\n"
                    )
                )

    @classmethod
    @timelog_getter
    def retrieve_log(cls):
        """Returns the log as a list, loading it from file if necessary."""
        return [entry for entry in cls._log.values()]

    @classmethod
    @timelog_getter
    def retrieve_from_log(cls, timestamp):
        """
        Returns an entry in the log based on timestamp,
        loading from file if necessary.
        """
        try:
            return cls._log[timestamp]
        except KeyError:
            logging.warning("Cannot access entry at invalid timestamp.")
            return None

    @classmethod
    @timelog_setter
    def add_to_log(cls, timestamp, hours, minutes, seconds, notes):
        """Add an entry to the log.
        If an entry with the timestamp is already in the log, one or more
        seconds will be added to the timestamp to resolve the conflict
        before creating and storing the entry.

        timestamp -- the timestamp as a datetime object
        hours -- the number of elapsed hours
        minutes -- the number of elapsed minutes
        seconds -- the number of elapsed seconds
        notes -- the activity description string for the entry

        Returns the timestamp the entry is stored under.
        """
        timestamp = LogEntry.normalize_timestamp(timestamp)
        # If/While the timestamp is already in the log...
        while timestamp in cls._log:
            # Resolve collision by incrementing it by one second.
            timestamp = cls.increment_timestamp(timestamp)

        # Create the new entry.
        entry = LogEntry()
        entry.set_timestamp(timestamp)
        entry.set_duration(hours, minutes, seconds)
        entry.set_notes(notes)

        # Add the new entry to the log.
        cls._log[timestamp] = entry

        return timestamp

    @classmethod
    @timelog_setter
    def remove_from_log(cls, timestamp):
        """Remove an entry from the log.

        timestamp -- the index of the item to remove
        """
        try:
            del cls._log[timestamp]
        except KeyError:
            logging.warning("Cannot delete entry at invalid timestamp.")
