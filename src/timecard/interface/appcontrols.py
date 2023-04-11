"""App Controls [Timecard]
Author(s): Jason C. McDonald

Allows switching between major application views.
"""

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWhatsThis, QWidget

from timecard.interface.quitview import QuitView
from timecard.interface.workspace import Workspace


class AppControls:
    widget = QWidget()
    layout = QHBoxLayout()
    btn_settings = QPushButton()
    btn_about = QPushButton()
    btn_help = QPushButton()
    btn_quit = QPushButton()

    @classmethod
    def build(cls):
        """Construct the interface."""
        cls.widget.setLayout(cls.layout)
        cls.layout.addWidget(cls.btn_settings)
        cls.layout.addWidget(cls.btn_about)
        cls.layout.addWidget(cls.btn_help)
        cls.layout.addWidget(cls.btn_quit)

        QuitView.connect(on_notquit=cls.default)

        cls._set_mode_default()

        return cls.widget

    @classmethod
    def _disconnect_buttons(cls):
        """Disconnect signals from the control buttons.
        This must be done before new signals can be added properly.
        """
        try:
            cls.btn_settings.clicked.disconnect()
        except RuntimeError:
            pass

        try:
            cls.btn_about.clicked.disconnect()
        except RuntimeError:
            pass

        try:
            cls.btn_help.clicked.disconnect()
        except RuntimeError:
            pass

        try:
            cls.btn_quit.clicked.disconnect()
        except RuntimeError:
            pass

    @classmethod
    def _set_mode_default(cls):
        """Set buttons to those for Log (default) mode."""
        cls._disconnect_buttons()

        cls.btn_settings.setText("Settings")
        cls.btn_settings.setIcon(QIcon.fromTheme("preferences-system"))
        cls.btn_settings.setWhatsThis("View and edit settings.")
        cls.btn_settings.clicked.connect(cls.settings)

        cls.btn_about.setText("About")
        cls.btn_about.setIcon(QIcon.fromTheme("help-about"))
        cls.btn_about.setWhatsThis("View Timecard credits and license.")
        cls.btn_about.clicked.connect(cls.about)

        cls.btn_help.setText("Help")
        cls.btn_help.setIcon(QIcon.fromTheme("help-contents"))
        cls.btn_help.setWhatsThis("Display help for a clicked item.")
        cls.btn_help.clicked.connect(cls.help)

        cls.btn_quit.setText("Quit")
        cls.btn_quit.setIcon(QIcon.fromTheme("application-exit"))
        cls.btn_quit.setWhatsThis("Quit Timecard.")
        cls.btn_quit.clicked.connect(cls.quit)

    @classmethod
    def _set_mode_settings(cls):
        """Set buttons to those for Settings mode."""
        cls._disconnect_buttons()

        cls.btn_settings.setText("Log")
        cls.btn_settings.setIcon(QIcon.fromTheme("go-home"))
        cls.btn_settings.setWhatsThis("Return to time log.")
        cls.btn_settings.clicked.connect(cls.default)

        cls.btn_about.setText("About")
        cls.btn_about.setIcon(QIcon.fromTheme("help-about"))
        cls.btn_about.setWhatsThis("View Timecard credits and license.")
        cls.btn_about.clicked.connect(cls.about)

        cls.btn_help.setText("Help")
        cls.btn_help.setIcon(QIcon.fromTheme("help-contents"))
        cls.btn_help.setWhatsThis("Display help for a clicked item.")
        cls.btn_help.clicked.connect(cls.help)

        cls.btn_quit.setText("Quit")
        cls.btn_quit.setIcon(QIcon.fromTheme("application-exit"))
        cls.btn_quit.setWhatsThis("Quit Timecard.")
        cls.btn_quit.clicked.connect(cls.quit)

    @classmethod
    def _set_mode_about(cls):
        """Set buttons to those for About mode."""
        cls._disconnect_buttons()

        cls.btn_settings.setText("Settings")
        cls.btn_settings.setIcon(QIcon.fromTheme("preferences-system"))
        cls.btn_settings.setWhatsThis("View and edit settings.")
        cls.btn_settings.clicked.connect(cls.settings)

        cls.btn_about.setText("Log")
        cls.btn_about.setIcon(QIcon.fromTheme("go-home"))
        cls.btn_about.setWhatsThis("Return to time log.")
        cls.btn_about.clicked.connect(cls.default)

        cls.btn_help.setText("Help")
        cls.btn_help.setIcon(QIcon.fromTheme("help-contents"))
        cls.btn_help.setWhatsThis("Display help for a clicked item.")
        cls.btn_help.clicked.connect(cls.help)

        cls.btn_quit.setText("Quit")
        cls.btn_quit.setIcon(QIcon.fromTheme("application-exit"))
        cls.btn_quit.setWhatsThis("Quit Timecard.")
        cls.btn_quit.clicked.connect(cls.quit)

    @classmethod
    def _set_mode_quit(cls):
        """Set buttons to those for Quit Prompt mode."""
        cls._disconnect_buttons()

        cls.btn_settings.setText("Settings")
        cls.btn_settings.setIcon(QIcon.fromTheme("preferences-system"))
        cls.btn_settings.setWhatsThis("View and edit settings.")
        cls.btn_settings.clicked.connect(cls.settings)

        cls.btn_about.setText("About")
        cls.btn_about.setIcon(QIcon.fromTheme("help-about"))
        cls.btn_about.setWhatsThis("View Timecard credits and license.")
        cls.btn_about.clicked.connect(cls.about)

        cls.btn_help.setText("Help")
        cls.btn_help.setIcon(QIcon.fromTheme("help-contents"))
        cls.btn_help.setWhatsThis("Display help for a clicked item.")
        cls.btn_help.clicked.connect(cls.help)

        cls.btn_quit.setText("Log")
        cls.btn_quit.setIcon(QIcon.fromTheme("go-home"))
        cls.btn_quit.setWhatsThis("Return to time log.")
        cls.btn_quit.clicked.connect(cls.default)

    @classmethod
    def default(cls):
        cls._set_mode_default()
        Workspace.set_mode_timelog()

    @classmethod
    def about(cls):
        cls._set_mode_about()
        Workspace.set_mode_about()

    @classmethod
    def settings(cls):
        cls._set_mode_settings()
        Workspace.set_mode_settings()

    @classmethod
    def help(cls):
        QWhatsThis.enterWhatsThisMode()

    @classmethod
    def quit(cls):
        cls._set_mode_quit()
        Workspace.set_mode_quit()
