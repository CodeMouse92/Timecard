from PySide2.QtCore import QTime, QTimer
from PySide2.QtWidgets import QLCDNumber


class TimeDisplay:

    lcd = QLCDNumber(8)
    timer = None
    time = None
    freeze = 0

    @classmethod
    def build(cls):
        """
        Build the time display GUI
        """
        cls.show_default()
        cls.lcd.setMinimumSize(0, 100)
        return cls.lcd

    @classmethod
    def show_default(cls):
        """
        Reset the time display to 00:00:00
        """
        cls.show_time()

    @classmethod
    def show_time(cls, hours=0, minutes=0, seconds=0):
        """
        Show the indicated time on the GUI.
        """
        cls.lcd.display(f"{hours:02}:{minutes:02}:{seconds:02}")

    @classmethod
    def update_time(cls):
        """
        Show the current elapsed time on the GUI.
        """
        cls.show_time(*cls.get_time())

    @classmethod
    def start_time(cls):
        """
        Start or resume the timer.
        """
        if cls.timer is None:
            cls.timer = QTimer(cls.lcd)
            cls.timer.timeout.connect(cls.update_time)
        if cls.time is None:
            cls.time = QTime()
            cls.time.start()
            cls.freeze = 0
        else:
            cls.time.restart()
        cls.timer.start()

    @classmethod
    def stop_time(cls):
        if cls.time is not None:
            cls.freeze += cls.time.elapsed()

        if cls.timer is not None:
            cls.timer.stop()

    @classmethod
    def reset_time(cls):
        """
        Prepare timer for reset, without erasing the last session's time.
        """
        cls.timer = None
        cls.time = None

    @classmethod
    def get_time_ms(cls):
        if cls.time:
            return cls.time.elapsed() + cls.freeze
        return cls.freeze

    @classmethod
    def get_time(cls):
        elapsed = cls.get_time_ms()
        seconds = elapsed // 1000

        minutes = seconds // 60
        seconds -= minutes * 60

        hours = minutes // 60
        minutes -= hours * 60

        return (hours, minutes, seconds)
