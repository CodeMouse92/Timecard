from PySide2.QtWidgets import QLineEdit


class Notes:
    txt_notes = QLineEdit()

    @classmethod
    def build(cls):
        cls.txt_notes.setPlaceholderText("What are you doing?")
        return cls.txt_notes

    @classmethod
    def get_text(cls):
        return cls.txt_notes.text()
