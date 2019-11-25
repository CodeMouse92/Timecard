import logging

from PySide2.QtWidgets import (
    QApplication, QSystemTrayIcon, QVBoxLayout, QWidget
)


class App:
    app = QApplication()
    window = QWidget()
    layout = QVBoxLayout()
    systray = QSystemTrayIcon()

    @classmethod
    def run(cls):
        if cls.app is None:
            return None

        cls.show_window()
        cls.show_systray()

        return cls.app.exec_()

    @classmethod
    def build(cls):
        logging.debug("Building main window.")
        cls._build_window()
        cls._build_systray()

    @classmethod
    def _build_window(cls):
        cls.window.resize(320, 400)
        cls.window.setWindowTitle(
            QApplication.translate("program_name", "Timecard")
        )
        # TODO: Set window tray
        cls.window.setLayout(cls.layout)

    @classmethod
    def _build_systray(cls):
        # TODO: Set sys tray icon
        pass

    @classmethod
    def show_window(cls):
        cls.window.show()

    @classmethod
    def hide_window(cls):
        cls.window.hide()

    @classmethod
    def show_systray(cls):
        cls.systray.show()

    @classmethod
    def hide_systray(cls):
        cls.systray.hide()

    @classmethod
    def add_widget(cls, widget):
        cls.layout.addWidget(widget)
