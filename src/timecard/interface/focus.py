"""Focus Notifications [Timecard]
Author(s): Jason C. McDonald

Display popup notifications to check if the user is focusing.
"""

import random
import string

from timecard.data.settings import Settings
from timecard.interface.notes import Notes
from timecard.interface.systray import SysTray
from timecard.interface.timedisplay import TimeDisplay


class Focus:
    prompt_with_note = [
        string.Template("Are you still focusing on $task?"),
        string.Template("Are you focused on $task?"),
        string.Template("You are tracking time on $task."),
        string.Template("Is $task still your focus?"),
        string.Template("Hey there! How is $task going?"),
    ]

    prompt_no_note = [
        "Are you still focusing?",
        "How's your focus right now?",
        "You are still tracking time.",
        "Hi there! Still focusing okay?",
    ]

    interval = 0
    randomize = False
    last_at = 0
    next_at = 0

    @classmethod
    def initialize(cls):
        """Initialize focus popup notification system."""
        cls.reload_settings()
        TimeDisplay.connect(on_minute=cls.notify)

    @classmethod
    def reload_settings(cls):
        """Reloads the settings and updates accordingly."""
        cls.interval, cls.randomize = Settings.get_focus()
        cls.calculate_next()

    @classmethod
    def calculate_next(cls):
        """Determine and store the next time a reminder shows."""
        if not cls.interval:
            cls.next_at = 0
            return
        if cls.randomize:
            offset = int(cls.interval * 0.2)
            interval = cls.interval + random.randint(-offset, offset)
        else:
            interval = cls.interval
        cls.next_at = cls.last_at + interval

    @classmethod
    def check(cls):
        """Check if it's time to show a notification."""
        if not cls.interval:
            return
        if TimeDisplay.get_time_min() >= cls.next_at:
            return True
        return False

    @classmethod
    def notify(cls, hours, minutes, seconds):
        """Display notification."""
        if not cls.check():
            return
        cls.last_at = TimeDisplay.get_time_min()
        activity = Notes.get_text()
        if activity:
            message = random.choice(cls.prompt_with_note).substitute(
                task=activity
            )
        else:
            message = random.choice(cls.prompt_no_note)

        # Show the notification
        SysTray.popup(message)
        # Determine when next notification should appear
        cls.calculate_next()
