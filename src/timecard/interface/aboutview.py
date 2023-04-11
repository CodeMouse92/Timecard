"""About View [Timecard]
Author(s): Jason C. McDonald

Displays "about" data for Timecard.
"""

from importlib import resources
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QWidget


class AboutView:
    widget = QWidget()
    layout = QVBoxLayout()
    lbl_info = QTextEdit()

    @classmethod
    def build(cls):
        """Build the interface."""
        cls.lbl_info = QTextEdit()

        about_file = Path(
            resources.files("timecard.resources").joinpath("about.txt")
        )
        try:
            with about_file.open("r", encoding="utf-8") as file:
                cls.lbl_info.setPlainText(file.read())
        except FileNotFoundError:
            cls.lbl_info.setPlainText(
                "TIMECARD\n"
                "Created by Jason C. McDonald\n\n"
                "ERROR: `resources/about.txt` missing"
            )
        cls.lbl_info.setWhatsThis("Credits and license for Timecard.")
        cls.lbl_info.setReadOnly(True)
        cls.lbl_info.setAlignment(Qt.AlignCenter)

        cls.widget.setLayout(cls.layout)
        cls.layout.addWidget(cls.lbl_info)

        return cls.widget
