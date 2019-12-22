from PySide2.QtWidgets import QMenu, QSystemTrayIcon
from PySide2.QtGui import QIcon

from timecard.interface.app import App
from timecard.interface.workspace import Workspace


class SysTray:

    systray = QSystemTrayIcon()
    menu = QMenu()

    @classmethod
    def build(cls):
        """Construct the system tray"""
        cls.systray.setIcon(App.icon)
        cls.menu.addAction(
            QIcon.fromTheme('view-restore'),
            "Show/Hide Window",
            cls.toggle_window
        )
        cls.menu.addSeparator()
        cls.menu.addAction(
            QIcon.fromTheme('application-exit'),
            "Quit Timecard...",
            cls.quit
        )

        cls.systray.setContextMenu(cls.menu)
        cls.systray.show()

        return cls.systray

    @classmethod
    def toggle_window(cls):
        App.toggle_window()

    @classmethod
    def quit(cls):
        App.show_window()
        Workspace.set_mode_quit()
