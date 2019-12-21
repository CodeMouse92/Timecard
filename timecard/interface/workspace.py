from PySide2.QtWidgets import QWidget, QStackedLayout

from timecard.interface.about import About
from timecard.interface.logview import LogView
from timecard.interface.settingspanel import SettingsPanel
from timecard.interface.quit import QuitPrompt


class Workspace:

    widget = QWidget()
    layout = QStackedLayout()
    previous = None

    @classmethod
    def build(cls):
        cls.widget.setLayout(cls.layout)
        cls.layout.addWidget(LogView.build())
        cls.layout.addWidget(About.build())
        cls.layout.addWidget(SettingsPanel.build())
        cls.layout.addWidget(QuitPrompt.build())

        return cls.widget

    @classmethod
    def set_mode_timelog(cls):
        cls.layout.setCurrentIndex(0)

    @classmethod
    def set_mode_about(cls):
        cls.layout.setCurrentIndex(1)

    @classmethod
    def set_mode_settings(cls):
        cls.layout.setCurrentIndex(2)

    @classmethod
    def set_mode_quit(cls):
        cls.layout.setCurrentIndex(3)
