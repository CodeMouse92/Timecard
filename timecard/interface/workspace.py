from PySide2.QtWidgets import QWidget, QStackedLayout

from timecard.interface.about import About
from timecard.interface.logview import LogView


class Workspace:

    widget = QWidget()
    layout = QStackedLayout()

    @classmethod
    def build(cls):
        cls.widget.setLayout(cls.layout)
        cls.layout.addWidget(LogView.build())
        cls.layout.addWidget(About.build())

        return cls.widget

    @classmethod
    def set_mode_timelog(cls):
        cls.layout.setCurrentIndex(0)

    @classmethod
    def set_mode_about(cls):
        cls.layout.setCurrentIndex(1)
