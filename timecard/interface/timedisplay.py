from PySide2.QtWidgets import QLCDNumber


class TimeDisplay:

    lcd = QLCDNumber(8)

    @classmethod
    def build(cls):
        cls.show_default()
        cls.lcd.setMinimumSize(0, 100)
        return cls.lcd

    @classmethod
    def show_default(cls):
        cls.show_time()

    @classmethod
    def show_time(cls, hours=0, minutes=0, seconds=0):
        cls.lcd.display(f"{hours:02}:{minutes:02}:{seconds:02}")
