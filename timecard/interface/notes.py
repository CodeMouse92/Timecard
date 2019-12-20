from PySide2.QtWidgets import QLineEdit


class Notes:
    txt_notes = QLineEdit()

    @classmethod
    def build(cls):
        """Build the notes interface."""
        cls.txt_notes.setPlaceholderText("What are you doing?")
        return cls.txt_notes

    @classmethod
    def get_text(cls):
        """Returns the current text in the notes box."""
        return cls.txt_notes.text()

    @classmethod
    def clear(cls):
        """Clears the notes box."""
        cls.txt_notes.clear()
