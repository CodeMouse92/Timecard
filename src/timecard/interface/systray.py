"""System Tray [Timecard]
Author(s): Jason C. McDonald

The application system tray and its menu.
"""

from PySide2.QtWidgets import QAction, QMenu, QSystemTrayIcon
from PySide2.QtGui import QIcon

from timecard.interface.app import App
from timecard.interface.timecontrols import TimeControls
from timecard.interface.timedisplay import TimeDisplay


class SysTray:
    systray = QSystemTrayIcon()
    menu = QMenu()

    act_status = QAction()
    act_time = QAction()
    act_toggle = QAction()
    act_quit = QAction()

    @classmethod
    def build(cls):
        """Construct the system tray"""
        cls.systray.setIcon(App.icon)

        cls.act_status.setText("00:00:00")
        cls.menu.addAction(cls.act_status)

        cls.menu.addAction(cls.act_time)
        cls.set_mode_stopped()

        cls.menu.addSeparator()

        cls.act_toggle.setIcon(QIcon.fromTheme('view-restore'))
        cls.act_toggle.setText("Show/Hide Window")
        cls.act_toggle.triggered.connect(cls.toggle_window)
        cls.menu.addAction(cls.act_toggle)

        cls.menu.addSeparator()

        cls.act_quit.setIcon(QIcon.fromTheme('application-exit'))
        cls.act_quit.setText("Quit Timecard")
        cls.act_quit.triggered.connect(cls.quit_app)
        cls.menu.addAction(cls.act_quit)

        cls.systray.setContextMenu(cls.menu)
        cls.systray.show()

        TimeDisplay.subscribe(cls.update_time)
        TimeControls.connect(
            start=cls.set_mode_running,
            resume=cls.set_mode_running,
            pause=cls.set_mode_paused,
            stop=cls.set_mode_save,
            save=cls.set_mode_stopped,
            reset=cls.set_mode_stopped
        )
        App.connect(notify=cls.popup)

        return cls.systray

    @classmethod
    def popup(cls, message):
        cls.systray.showMessage("Timecard", message, App.icon)

    @classmethod
    def update_time(cls, hours=0, minutes=0, seconds=0):
        cls.act_status.setText(f"{hours:02}:{minutes:02}:{seconds:02}")

    @classmethod
    def _disconnect_actions(cls):
        """Disconnect signals for any actions that are modified by timer."""
        try:
            cls.act_time.triggered.disconnect()
        except RuntimeError:
            pass

    @classmethod
    def set_mode_stopped(cls):
        cls._disconnect_actions()
        cls.act_quit.setEnabled(True)
        cls.act_time.setEnabled(True)
        cls.act_time.setText("Start")
        cls.act_time.setIcon(QIcon.fromTheme('media-playback-start'))
        cls.act_time.triggered.connect(TimeControls.start)

    @classmethod
    def set_mode_running(cls):
        cls._disconnect_actions()
        cls.act_quit.setEnabled(False)
        cls.act_time.setEnabled(True)
        cls.act_time.setText("Pause")
        cls.act_time.setIcon(QIcon.fromTheme('media-playback-pause'))
        cls.act_time.triggered.connect(TimeControls.pause)

    @classmethod
    def set_mode_paused(cls):
        cls._disconnect_actions()
        cls.act_quit.setEnabled(False)
        cls.act_time.setEnabled(True)
        cls.act_time.setText("Resume")
        cls.act_time.setIcon(QIcon.fromTheme('media-playback-start'))
        cls.act_time.triggered.connect(TimeControls.resume)

    @classmethod
    def set_mode_save(cls):
        cls._disconnect_actions()
        cls.act_quit.setEnabled(False)
        cls.act_time.setEnabled(False)
        cls.act_time.setText("Awaiting Save")

    @classmethod
    def toggle_window(cls):
        App.toggle_window()

    @classmethod
    def quit_app(cls):
        App.quit()

    @classmethod
    def connect(cls, toggle=None, quit=None):
        cls.toggle_callback = toggle
        cls.quit_callback = quit
