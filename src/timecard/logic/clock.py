"""Clock [Timecard]
Author(s): Jason C. McDonald

The core clock/timer functionality, to which pretty much everything else connects.
"""

from PySide6.QtCore import QTimer


class Clock:
    clock = None
    callback_tick = []

    @classmethod
    def start(cls):
        """Start the clock."""
        cls.clock = QTimer()
        cls.clock.timeout.connect(cls.tick)
        cls.clock.start(1000)  # tick once every second (performance!)

    @classmethod
    def tick(cls):
        """Fires once every second."""
        for callback in cls.callback_tick:
            callback()

    @classmethod
    def connect(cls, on_tick):
        """Connect signal."""
        if on_tick and on_tick not in cls.callback_tick:
            cls.callback_tick.append(on_tick)

    @classmethod
    def disconnect(cls, on_tick):
        """Disconnect callback from signal. (Idempotent)."""
        try:
            cls.callback_tick.remove(on_tick)
        except ValueError:
            pass
