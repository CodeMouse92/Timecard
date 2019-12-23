import logging
from pathlib import Path

from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget
from PySide2.QtGui import QIcon


class MainWindow(QWidget):
    def closeEvent(self, event):
        """Hide the window on close."""
        App.hide_window()
        event.ignore()
        # TODO: Show popup to notify about the tray
        # TODO: Use a setting to determine this behavior?


class App:
    app = QApplication()
    window = MainWindow()
    layout = QVBoxLayout()
    icon = QIcon(str(Path('timecard', 'resources', 'timecard.svg')))

    notify_callback = None

    @classmethod
    def run(cls):
        """Run the application."""
        if cls.app is None:
            return None

        cls.show_window()

        return cls.app.exec_()

    @classmethod
    def build(cls):
        """Construct the interface."""
        logging.debug("Building main window.")
        cls.window.resize(380, 400)
        cls.window.setWindowTitle(
            QApplication.translate("program_name", "Timecard")
        )
        cls.window.setWindowIcon(cls.icon)
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

    @classmethod
    def hide_window(cls):
        """Hide the main window."""
        cls.window.hide()
        cls.notify("Timecard is still available in the notification area.")

    @classmethod
    def add_widget(cls, widget):
        """Add a widget to the main window."""
        cls.layout.addWidget(widget)

    @classmethod
    def notify(cls, message):
        if cls.notify_callback:
            cls.notify_callback(message)

    @classmethod
    def connect(cls, /, notify=None):
        if notify:
            cls.notify_callback = notify

    @classmethod
    def quit(cls):
        cls.app.quit()
