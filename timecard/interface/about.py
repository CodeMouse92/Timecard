from pathlib import Path

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QVBoxLayout, QTextEdit


class About:
    widget = QWidget()
    layout = QVBoxLayout()
    lbl_info = QTextEdit()

    @classmethod
    def build(cls):
        """Build the interface."""
        cls.lbl_info = QTextEdit()

        about_file = Path('timecard', 'resources', 'about.txt')
        try:
            with about_file.open('r') as file:
                cls.lbl_info.setPlainText(file.read())
        except FileNotFoundError:
            cls.lbl_info.setPlainText("TIMECARD\n"
                                      "Created by Jason C. McDonald\n\n"
                                      "ERROR: `resources/about.txt` missing")
        cls.lbl_info.setWhatsThis("Credits and license for Timecard.")
        cls.lbl_info.setReadOnly(True)
        cls.lbl_info.setAlignment(Qt.AlignCenter)

        cls.widget.setLayout(cls.layout)
        cls.layout.addWidget(cls.lbl_info)

        return cls.widget
