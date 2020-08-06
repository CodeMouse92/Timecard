"""Quit View [Timecard]
Author(s): Jason C. McDonald

Prompts the user whether they want to quit or not.
"""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton
from PySide2.QtGui import QIcon

from timecard.interface.app import App


class QuitView:
    widget = QWidget()
    layout = QGridLayout()
    lbl_prompt = QLabel()
    btn_yes = QPushButton()
    btn_no = QPushButton()
    callback = None

    @classmethod
    def build(cls):
        """Build the interface."""
        cls.layout.addWidget(cls.lbl_prompt, 0, 0, 1, 2)
        cls.layout.addWidget(cls.btn_no, 1, 0)
        cls.layout.addWidget(cls.btn_yes, 1, 1)

        cls.lbl_prompt.setText("Are you SURE you want to quit?\n"
                               "Any unsaved time will be lost.")
        cls.lbl_prompt.setAlignment(Qt.AlignCenter)

        cls.btn_no.setIcon(QIcon.fromTheme('go-previous'))
        cls.btn_no.setText("Keep Going")
        cls.btn_no.setWhatsThis("Return to time log view.")
        cls.btn_no.clicked.connect(cls.no)

        cls.btn_yes.setIcon(QIcon.fromTheme('application-exit'))
        cls.btn_yes.setText("Quit")
        cls.btn_yes.setWhatsThis("Quit Timecard.")
        cls.btn_yes.clicked.connect(cls.yes)

        cls.widget.setLayout(cls.layout)
        return cls.widget

    @classmethod
    def connect(cls, callback):
        cls.callback = callback

    @classmethod
    def no(cls):
        """Do NOT quit the program."""
        if cls.callback:
            cls.callback()

    @classmethod
    def yes(cls):
        """Quit the program."""
        App.quit()
