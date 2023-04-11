"""Time Display [Timecard]
Author(s): Jason C. McDonald

Displays and stores the current timer duration, including its start timestamp
and state.
"""

from datetime import datetime

from PySide6.QtCore import QDate, QDateTime, QElapsedTimer, QTime
from PySide6.QtWidgets import QLCDNumber

from timecard.logic.clock import Clock


class TimeDisplay:
    lcd = QLCDNumber(8)
    time = None
    timestamp = None
    # Stored time in ms from prior pause(s)
    freeze = 0
    paused = False

    from_backup = False

    callback_tick = []
    callback_minute = []
    callback_stop = []

    @classmethod
    def build(cls):
        """Build the time display GUI."""
        cls.lcd.setWhatsThis(
            "The time elapsed on the current timer. " "(Hours:Minutes:Seconds)"
        )
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
            QTime(timestamp.hour, timestamp.minute, timestamp.second),
        )
        # Restore the duration
        cls.freeze = elapsed
        # Force the user to either save or reset. Resuming makes no sense.
        cls.paused = False
        # Show the time.
        cls.show_time(*cls.get_time())

    @classmethod
    def show_default(cls):
        """Reset the time display to 00:00:00"""
        cls.show_time()

    @classmethod
    def show_time(cls, hours=0, minutes=0, seconds=0):
        """Show the indicated time on the GUI.

        hours -- the number of hours
        minutes -- the number of minutes
        seconds -- the number of seconds
        """
        cls.lcd.display(f"{hours:02}:{minutes:02}:{seconds:02}")

    @classmethod
    def tick(cls, hours, minutes, seconds):
        for callback in cls.callback_tick:
            callback(hours, minutes, seconds)
        if minutes and not seconds:
            for callback in cls.callback_minute:
                callback(hours, minutes, seconds)

    @classmethod
    def update_time(cls):
        """Show the current elapsed time on the GUI."""
        time = cls.get_time()
        cls.show_time(*time)
        cls.tick(*time)

    @classmethod
    def start_time(cls):
        """Start or resume the timer."""
        Clock.connect(on_tick=cls.update_time)
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

        cls.paused = False

    @classmethod
    def stop_time(cls):
        """Stop (paused) the timer."""
        if cls.paused:
            return

        if cls.time is not None:
            cls.freeze += cls.time.elapsed()

        Clock.disconnect(on_tick=cls.update_time)

        cls.paused = True

    @classmethod
    def reset_time(cls, erase=False):
        """Prepare timer for reset, optionally erasing the last session's time."""
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
    def get_time_min(cls):
        """Returns the current elapsed time in truncated minutes."""
        return cls.get_time_ms() // 1000 // 60

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
        timestamp = datetime(
            cls.timestamp.date().year(),
            cls.timestamp.date().month(),
            cls.timestamp.date().day(),
            cls.timestamp.time().hour(),
            cls.timestamp.time().minute(),
            cls.timestamp.time().second(),
        )
        return timestamp

    @classmethod
    def get_timestamp_string(cls):
        """Returns the timestamp as a storable string."""
        return (
            f"{cls.timestamp.date().year()}:"
            f"{cls.timestamp.date().month()}:"
            f"{cls.timestamp.date().day()}:"
            f"{cls.timestamp.time().hour()}:"
            f"{cls.timestamp.time().minute()}:"
            f"{cls.timestamp.time().second()}"
        )

    @classmethod
    def connect(cls, on_tick=None, on_minute=None, on_stop=None):
        """Subscribe to timer events.

        on_tick= fires every second. Callback must accept (hours, minutes, seconds)
        on_minute= fires every minute. Callback must accept (hours, minutes, seconds)
        on_stop= fires when the clock is stopped (not paused)
        """
        if on_tick and on_tick not in cls.callback_tick:
            cls.callback_tick.append(on_tick)
        if on_minute and on_minute not in cls.callback_minute:
            cls.callback_minute.append(on_minute)
        if on_stop and on_stop not in cls.callback_stop:
            cls.callback_stop.append(on_stop)
