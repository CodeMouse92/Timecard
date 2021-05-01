"""Time Display [Timecard]
Author(s): Jason C. McDonald

Displays and stores the current timer duration, including its start timestamp
and state.
"""

from datetime import datetime

from PySide2.QtCore import QDateTime, QDate, QTime, QElapsedTimer, QTimer
from PySide2.QtWidgets import QLCDNumber


class TimeDisplay:

    lcd = QLCDNumber(8)
    timer = None
    time = None
    timestamp = None
    # Stored time in ms from prior pause(s)
    freeze = 0
    paused = False

    from_backup = False

    callback_tick = []
    callback_stop = []

    @classmethod
    def build(cls):
        """Build the time display GUI."""
        cls.lcd.setWhatsThis("The time elapsed on the current timer. "
                             "(Hours:Minutes:Seconds)")
        cls.show_default()
        cls.lcd.setMinimumSize(0, 100)
        return cls.lcd

    @classmethod
    def restore_from_backup(cls, timestamp: datetime, elapsed):
        """Restore the timer state from backup."""
        # Just ignore less than a second of time.
        if elapsed < (1000):
            return

        # If loading from backup, indicate that fact so we don't clobber timestamp.
        cls.from_backup = True
        # Restore the timestamp.
        cls.timestamp = QDateTime(
            QDate(timestamp.year, timestamp.month, timestamp.day),
            QTime(timestamp.hour, timestamp.minute, timestamp.second)
        )
        # Restore the duration
        cls.freeze = elapsed
        # Force the user to either save or reset. Resuming makes no sense.
        cls.paused = False
        # Show the time.
        cls.show_time(*cls.get_time(), silent=True)

    @classmethod
    def show_default(cls):
        """Reset the time display to 00:00:00"""
        cls.show_time()

    @classmethod
    def show_time(cls, hours=0, minutes=0, seconds=0, silent=False):
        """Show the indicated time on the GUI.

        hours -- the number of hours
        minutes -- the number of minutes
        seconds -- the number of seconds

        silent -- don't fire callbacks
        """
        cls.lcd.display(f"{hours:02}:{minutes:02}:{seconds:02}")
        if not silent:
            for callback in cls.callback_tick:
                callback(hours, minutes, seconds)

    @classmethod
    def update_time(cls):
        """Show the current elapsed time on the GUI."""
        cls.show_time(*cls.get_time())

    @classmethod
    def start_time(cls):
        """Start or resume the timer."""
        if cls.timer is None:
            cls.timer = QTimer(cls.lcd)
            cls.timer.timeout.connect(cls.update_time)
        if cls.time is None:
            cls.time = QElapsedTimer()
            cls.time.start()

            # Do not clobber timestamp when restoring from backup
            if not cls.from_backup:
                cls.timestamp = QDateTime.currentDateTime()
            else:
                # After restoring from backup, forget about it.
                # We need to be able to create new timestamps afterward.
                cls.from_backup = False
        else:
            cls.time.restart()

        cls.timer.start(1000)  # tick once every second (performance!)
        cls.paused = False

    @classmethod
    def stop_time(cls):
        """Stop (paused) the timer."""
        if cls.paused:
            return

        if cls.time is not None:
            cls.freeze += cls.time.elapsed()

        if cls.timer is not None:
            cls.timer.stop()

        cls.paused = True

    @classmethod
    def reset_time(cls, erase=False):
        """Prepare timer for reset, optionally erasing the last session's time.
        """
        cls.timer = None
        cls.time = None
        if erase:
            cls.freeze = 0
        for callback in cls.callback_stop:
            callback(erase)

    @classmethod
    def get_time_ms(cls):
        """Returns the current elapsed time in milliseconds."""
        if cls.time:
            return cls.time.elapsed() + cls.freeze
        return cls.freeze

    @classmethod
    def get_time_ms_string(cls):
        return str(cls.get_time_ms())

    @classmethod
    def get_time(cls):
        """Returns the current elapsed time as a tuple
        (hours, minutes, seconds)
        """

        elapsed = cls.get_time_ms()
        seconds = elapsed // 1000

        minutes = seconds // 60
        seconds -= minutes * 60

        hours = minutes // 60
        minutes -= hours * 60

        return (hours, minutes, seconds)

    @classmethod
    def get_timestamp(cls):
        """Returns the timestamp of the last timer as a datetime object."""
        timestamp = datetime(cls.timestamp.date().year(),
                             cls.timestamp.date().month(),
                             cls.timestamp.date().day(),
                             cls.timestamp.time().hour(),
                             cls.timestamp.time().minute(),
                             cls.timestamp.time().second()
                             )
        return timestamp

    @classmethod
    def get_timestamp_string(cls):
        """Returns the timestamp as a storable string."""
        return (f"{cls.timestamp.date().year()}:"
                f"{cls.timestamp.date().month()}:"
                f"{cls.timestamp.date().day()}:"
                f"{cls.timestamp.time().hour()}:"
                f"{cls.timestamp.time().minute()}:"
                f"{cls.timestamp.time().second()}"
                )

    @classmethod
    def subscribe_tick(cls, callback=None):
        """Subscribe to every clock tick
        Callback callable must accept the arguments: (hours, minutes, seconds)
        """
        if callback:
            cls.callback_tick.append(callback)

    @classmethod
    def subscribe_stop(cls, callback=None):
        """Subscribe to the clock being stopped (not paused)
        Callback callable must accept the arguments: (erased: bool)
        """
        if callback:
            cls.callback_stop.append(callback)
