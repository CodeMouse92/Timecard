import logging

from PySide2.QtWidgets import (
    QApplication, QSystemTrayIcon, QVBoxLayout, QWidget
)


class MainWindow(QWidget):
    def closeEvent(self, event):
        """Handle the window being closed."""
        # TODO: Custom close handling here
        event.accept()


class App:
    app = QApplication()
    window = MainWindow()
    layout = QVBoxLayout()
    systray = QSystemTrayIcon()

    @classmethod
    def run(cls):
        """Run the application."""
        if cls.app is None:
            return None

        cls.show_window()
        cls.show_systray()

        return cls.app.exec_()

    @classmethod
    def build(cls):
        """Construct the interface."""
        logging.debug("Building main window.")
        cls._build_window()
        cls._build_systray()

    @classmethod
    def _build_window(cls):
        """Construct the window."""
        cls.window.resize(320, 400)
        cls.window.setWindowTitle(
            QApplication.translate("program_name", "Timecard")
        )
        # TODO: Set window icon
        cls.window.setLayout(cls.layout)

    @classmethod
    def _build_systray(cls):
        """Construct the system tray"""
        # TODO: Set sys tray icon
        pass

    @classmethod
    def show_window(cls):
        """Display the main window."""
        cls.window.show()

    @classmethod
    def hide_window(cls):
        """Hide the main window."""
        cls.window.hide()

    @classmethod
    def show_systray(cls):
        """Show the system tray."""
        cls.systray.show()

    @classmethod
    def hide_systray(cls):
        """Hide the system tray."""
        cls.systray.hide()

    @classmethod
    def add_widget(cls, widget):
        """Add a widget to the main window."""
        cls.layout.addWidget(widget)
