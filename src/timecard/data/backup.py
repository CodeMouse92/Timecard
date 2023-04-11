"""Backup [Timecard]
Author(s): Jason C. McDonald

Stores the current state of the program in a temporary file, in case of
crash or accidental quit.
"""

import logging
from datetime import datetime
from pathlib import Path
from time import sleep, time

from appdirs import user_cache_dir

from timecard.interface.notes import Notes
from timecard.interface.timecontrols import TimeControls
from timecard.interface.timedisplay import TimeDisplay


class Backup:
    _active = False
    # use the system epoch as a unique instance identifier
    _backup_dir = Path(user_cache_dir("timecard"))
    _instance_id = str(int(time()))
    _storage = _backup_dir / f"{_instance_id}.backup"
    _staging = _backup_dir / f"{_instance_id}.backup~"
    _query = _backup_dir / f"{_instance_id}.query"

    @classmethod
    def check_for_recall(cls):
        """Check if there is a backup that needs to be grabbed.
        If there are multiple backups, grab one (doesn't matter which)."""
        try:
            for backup in cls._backup_dir.glob("*.backup"):
                # Check for signs of life
                query = cls._backup_dir / f"{backup.stem}.query"
                # Create a query file to see if this instance ID is alive.
                query.touch(exist_ok=True)
                # Wait a literal second to let any other instances "respond"
                sleep(1)
                # If the other instance was alive, it would delete the query...
                if not query.exists():
                    # In that case, this one is occupied. Next!
                    continue

                with backup.open("r") as file:
                    recovered = [s.strip() for s in file.readlines()]

                    # Attempt to restore the recovered data.
                    timestamp = datetime(
                        *(int(v) for v in recovered[0].split(":"))
                    )
                    duration = int(recovered[1])
                    TimeDisplay.restore_from_backup(timestamp, duration)
                    notes = recovered[2]
                    Notes.restore_from_backup(notes)

                    # Allow the user to either reset or save.
                    TimeControls._set_mode_save()

                # Clear the file we just loaded.
                backup.unlink(missing_ok=True)
                query.unlink(missing_ok=True)

                # We are now done. Quit.
                return

        except StopIteration:
            return  # Nothing to load, move along.
        except (IndexError, ValueError):
            # Warn about corrupted backup
            logging.warning(f"Corrupted backup file: {cls._backup_dir}")
            # Delete corrupted backup file
            backup.unlink(missing_ok=True)
            # Try again...maybe a different file will work?
            cls.check_for_recall()

    @classmethod
    def remember(cls, hours, minutes, seconds):
        # Don't store when clock resets, only if minutes or hours has a value
        if hours or minutes:
            # Grab data in advance
            data = [
                TimeDisplay.get_timestamp_string() + "\n",
                TimeDisplay.get_time_ms_string() + "\n",
                Notes.get_text() + "\n",
            ]

            # Write data to staging file
            with cls._staging.open("w") as file:
                file.writelines(data)
            cls._staging.replace(cls._storage)  # Move into place

    @classmethod
    def forget(cls):
        """Clear backups for instance."""
        cls._storage.unlink(missing_ok=True)
        cls._staging.unlink(missing_ok=True)

    @classmethod
    def start_monitoring(cls):
        """Subscribe to the TimeDisplay events for purposes of backing up
        the timer in case of crash.
        """
        if cls._active:
            return

        cls._backup_dir.mkdir(parents=True, exist_ok=True)

        cls._active = True

        def tick(hours, minutes, seconds):
            # Prevent any other instances of Timecard from claiming recoveries
            cls._query.unlink(missing_ok=True)
            cls.remember(hours, minutes, seconds)

        def stop(erase):
            if erase:
                cls.forget()

        TimeDisplay.connect(on_minute=tick, on_stop=stop)
