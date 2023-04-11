"""Notes [Timecard]
Author(s): Jason C. McDonald

The box for entering session activity notes.
"""

from PySide6.QtWidgets import QLineEdit


class Notes:
    txt_notes = QLineEdit()

    @classmethod
    def build(cls):
        """Build the notes interface."""
        cls.txt_notes.setPlaceholderText("What are you doing?")
        cls.txt_notes.setWhatsThis(
            "A description for your current activity. "
            "This will be saved with the log entry."
        )
        return cls.txt_notes

    @classmethod
    def restore_from_backup(cls, notes):
        """Sets value from backup."""
        cls.txt_notes.setText(notes)

    @classmethod
    def get_text(cls):
        """Returns the current text in the notes box."""
        return cls.txt_notes.text()

    @classmethod
    def clear(cls):
        """Clears the notes box."""
        cls.txt_notes.clear()
