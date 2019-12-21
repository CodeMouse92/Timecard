from PySide2.QtWidgets import QPushButton, QHBoxLayout, QWidget
from PySide2.QtGui import QIcon

from timecard.interface.workspace import Workspace
from timecard.interface.quit import QuitPrompt

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

        QuitPrompt.connect(cls.default)

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

        cls.btn_settings.setText("")
        cls.btn_settings.setIcon(QIcon.fromTheme('preferences-system'))
        cls.btn_settings.clicked.connect(cls.settings)

        cls.btn_about.setText("")
        cls.btn_about.setIcon(QIcon.fromTheme('help-about'))
        cls.btn_about.clicked.connect(cls.about)

        cls.btn_help.setText("")
        cls.btn_help.setIcon(QIcon.fromTheme('help-contents'))
        cls.btn_help.clicked.connect(cls.settings)

        cls.btn_quit.setText("")
        cls.btn_quit.setIcon(QIcon.fromTheme('application-exit'))
        cls.btn_quit.clicked.connect(cls.quit)

    @classmethod
    def _set_mode_settings(cls):
        """Set buttons to those for Settings mode."""
        cls._disconnect_buttons()

        cls.btn_settings.setText("")
        cls.btn_settings.setIcon(QIcon.fromTheme('go-home'))
        cls.btn_settings.clicked.connect(cls.default)

        cls.btn_about.setText("")
        cls.btn_about.setIcon(QIcon.fromTheme('help-about'))
        cls.btn_about.clicked.connect(cls.about)

        cls.btn_help.setText("")
        cls.btn_help.setIcon(QIcon.fromTheme('help-contents'))
        cls.btn_help.clicked.connect(cls.help)

        cls.btn_quit.setText("")
        cls.btn_quit.setIcon(QIcon.fromTheme('application-exit'))
        cls.btn_quit.clicked.connect(cls.quit)

    @classmethod
    def _set_mode_about(cls):
        """Set buttons to those for About mode."""
        cls._disconnect_buttons()

        cls.btn_settings.setText("")
        cls.btn_settings.setIcon(QIcon.fromTheme('preferences-system'))
        cls.btn_settings.clicked.connect(cls.settings)

        cls.btn_about.setText("")
        cls.btn_about.setIcon(QIcon.fromTheme('go-home'))
        cls.btn_about.clicked.connect(cls.default)

        cls.btn_help.setText("")
        cls.btn_help.setIcon(QIcon.fromTheme('help-contents'))
        cls.btn_help.clicked.connect(cls.help)

        cls.btn_quit.setText("")
        cls.btn_quit.setIcon(QIcon.fromTheme('application-exit'))
        cls.btn_quit.clicked.connect(cls.quit)

    @classmethod
    def _set_mode_help(cls):
        pass

    @classmethod
    def _set_mode_quit(cls):
        """Set buttons to those for Quit Prompt mode."""
        cls._disconnect_buttons()

        cls.btn_settings.setText("")
        cls.btn_settings.setIcon(QIcon.fromTheme('preferences-system'))
        cls.btn_settings.clicked.connect(cls.settings)

        cls.btn_about.setText("")
        cls.btn_about.setIcon(QIcon.fromTheme('help-about'))
        cls.btn_about.clicked.connect(cls.about)

        cls.btn_help.setText("")
        cls.btn_help.setIcon(QIcon.fromTheme('help-contents'))
        cls.btn_help.clicked.connect(cls.help)

        cls.btn_quit.setText("")
        cls.btn_quit.setIcon(QIcon.fromTheme('go-home'))
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
        # Use "What's This" mode
        # https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWhatsThis.html
        pass

    @classmethod
    def quit(cls):
        cls._set_mode_quit()
        Workspace.set_mode_quit()
