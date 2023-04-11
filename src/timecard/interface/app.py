"""App [Timecard]
Author(s): Jason C. McDonald

The main application classes. Most of the interface modules rely on this,
so it should not rely on any other module in the interface subpackage.
"""

import logging
from importlib import resources

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from timecard.data.settings import Settings

VERSION = "3.0.0"

class MainWindow(QWidget):
    def closeEvent(self, event):
        """Hide the window on close."""
        if Settings.get_persist():
            App.hide_window()
            event.ignore()
        else:
            event.accept()


class App:
    app = QApplication()
    window = MainWindow()
    layout = QVBoxLayout()

    icon_path = str(
        resources.files("timecard.resources").joinpath("timecard.svg")
    )
    icon = QIcon(icon_path)

    hide_callback = []

    @classmethod
    def run(cls):
        """Run the application."""
        if cls.app is None:
            return None

        cls.show_window()

        return cls.app.exec_()

    @classmethod
    def build(cls):
        """Construct the application."""
        logging.debug("Building application.")
        cls.app.setApplicationName("Timecard")
        cls.app.setApplicationVersion(VERSION)
        cls.app.setDesktopFileName("com.codemouse92.timecard")
        cls.app.setWindowIcon(cls.icon)

        logging.debug("Building main window.")
        cls.window.resize(500, 400)
        cls.window.setLayout(cls.layout)

    @classmethod
    def toggle_window(cls):
        if cls.window.isVisible():
            cls.hide_window()
        else:
            cls.show_window()

    @classmethod
    def show_window(cls):
        """Display the main window."""
        cls.window.show()
        cls.window.activateWindow()
        cls.window.raise_()

    @classmethod
    def hide_window(cls):
        """Hide the main window."""
        cls.window.hide()
        for callback in cls.hide_callback:
            callback("Timecard is still running in the notification area.")

    @classmethod
    def add_widget(cls, widget):
        """Add a widget to the main window."""
        cls.layout.addWidget(widget)

    @classmethod
    def connect(cls, on_hide=None):
        if on_hide and on_hide not in cls.hide_callback:
            cls.hide_callback.append(on_hide)

    @classmethod
    def quit(cls):
        cls.app.quit()
