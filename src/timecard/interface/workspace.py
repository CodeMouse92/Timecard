"""Workspace [Timecard]
Author(s): Jason C. McDonald

Switches between Views in the application.
"""

from PySide6.QtWidgets import QStackedLayout, QWidget

from timecard.interface.aboutview import AboutView
from timecard.interface.editview import EditView
from timecard.interface.logview import LogView
from timecard.interface.quitview import QuitView
from timecard.interface.settingsview import SettingsView


class Workspace:
    widget = QWidget()
    layout = QStackedLayout()
    previous = None

    @classmethod
    def build(cls):
        cls.widget.setLayout(cls.layout)
        cls.layout.addWidget(LogView.build())
        cls.layout.addWidget(AboutView.build())
        cls.layout.addWidget(SettingsView.build())
        cls.layout.addWidget(QuitView.build())
        cls.layout.addWidget(EditView.build())

        LogView.connect(on_edit=cls.set_mode_edit)
        EditView.connect(on_done=cls.edit_done)

        return cls.widget

    @classmethod
    def set_mode_timelog(cls):
        cls.layout.setCurrentIndex(0)
        LogView.refresh()

    @classmethod
    def set_mode_about(cls):
        cls.layout.setCurrentIndex(1)

    @classmethod
    def set_mode_settings(cls):
        cls.layout.setCurrentIndex(2)

    @classmethod
    def set_mode_quit(cls):
        cls.layout.setCurrentIndex(3)

    @classmethod
    def set_mode_edit(cls, entry):
        cls.layout.setCurrentIndex(4)
        EditView.load_item(entry)

    @classmethod
    def edit_done(cls):
        LogView.unselected()
        cls.set_mode_timelog()
