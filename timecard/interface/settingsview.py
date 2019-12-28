"""Settings View [Timecard]
Author(s): Jason C. McDonald

Allows viewing and editing application settings.
"""

from datetime import datetime

from PySide2.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout
from PySide2.QtWidgets import QLabel, QCheckBox, QLineEdit, QPushButton
from PySide2.QtGui import QIcon

from timecard.data.timelog import TimeLog
from timecard.data.settings import Settings


class SettingsView:
    widget = QWidget()
    layout = QVBoxLayout()
    grid_widget = QWidget()
    grid_layout = QGridLayout()
    buttons_widget = QWidget()
    buttons_layout = QHBoxLayout()

    lbl_logdir = QLabel("Log Directory")
    txt_logdir = QLineEdit()
    lbl_logname = QLabel("Log Name")
    txt_logname = QLineEdit()
    chk_persist = QCheckBox("Keep in Notification Area")
    lbl_datefmt = QLabel("Timestamp Format")
    txt_datefmt = QLineEdit()
    lbl_datefmt_test = QLabel()
    chk_decdur = QCheckBox("Show Duration as Decimal")

    btn_revert = QPushButton(QIcon.fromTheme('edit-undo'), "Revert")
    btn_save = QPushButton(QIcon.fromTheme('document-save'), "Save")

    reload_log = False

    @classmethod
    def build(cls):
        """Build the interface."""
        cls.txt_logdir.textEdited.connect(cls.edited)
        cls.txt_logdir.textEdited.connect(cls.logpath_edited)
        cls.lbl_logdir.setWhatsThis("The directory where the logs are saved.")
        cls.txt_logdir.setWhatsThis("The directory where the logs are saved.")
        cls.txt_logname.textEdited.connect(cls.edited)
        cls.txt_logname.textEdited.connect(cls.logpath_edited)
        cls.lbl_logname.setWhatsThis("The filename for the log.")
        cls.txt_logname.setWhatsThis("The filename for the log.")

        cls.chk_persist.stateChanged.connect(cls.edited)
        cls.chk_persist.setWhatsThis("When window is closed, keep application "
                                     "running in notification area. WARNING: "
                                     "If unchecked, closing the window will "
                                     "immediately quit, discarding any "
                                     "unsaved time.")

        cls.txt_datefmt.textEdited.connect(cls.edited)
        cls.txt_datefmt.textEdited.connect(cls.datefmt_edited)
        cls.lbl_datefmt.setWhatsThis("The format for the timestamp. "
                                     "Uses 1989 C standard.")
        cls.txt_datefmt.setWhatsThis("The format for the timestamp. "
                                     "Uses 1989 C standard.")
        cls.lbl_datefmt_test.setWhatsThis("Preview of the timestamp format. "
                                          "Displays: 02 Jan 1998 14:30:25")

        cls.chk_decdur.stateChanged.connect(cls.edited)
        cls.chk_decdur.setWhatsThis("Display duration in log as decimal "
                                    "instead of HH:MM:SS. (Ignores seconds.)")

        cls.grid_layout.addWidget(cls.lbl_logdir, 0, 0)
        cls.grid_layout.addWidget(cls.txt_logdir, 0, 1)
        cls.grid_layout.addWidget(cls.lbl_logname, 1, 0)
        cls.grid_layout.addWidget(cls.txt_logname, 1, 1)
        cls.grid_layout.addWidget(cls.chk_persist, 2, 1)
        cls.grid_layout.addWidget(cls.lbl_datefmt, 3, 0)
        cls.grid_layout.addWidget(cls.txt_datefmt, 3, 1)
        cls.grid_layout.addWidget(cls.lbl_datefmt_test, 4, 1)
        cls.grid_layout.addWidget(cls.chk_decdur, 5, 1)
        cls.grid_widget.setLayout(cls.grid_layout)

        cls.buttons_layout.addWidget(cls.btn_revert)
        cls.buttons_layout.addWidget(cls.btn_save)
        cls.btn_save.clicked.connect(cls.save)
        cls.btn_save.setWhatsThis("Save the settings.")
        cls.btn_revert.clicked.connect(cls.refresh)
        cls.btn_revert.setWhatsThis("Discard changes to settings.")

        cls.buttons_widget.setLayout(cls.buttons_layout)
        cls.layout.addWidget(cls.grid_widget)
        cls.layout.addWidget(cls.buttons_widget)
        cls.widget.setLayout(cls.layout)

        cls.refresh()
        return cls.widget

    @classmethod
    def logpath_edited(cls):
        """Schedule reload of log."""
        cls.reload_log = True

    @classmethod
    def datefmt_edited(cls):
        """Update the preview for the timestamp format."""
        test = datetime(1998, 1, 2, 14, 30, 25, 0)
        cls.lbl_datefmt_test.setText(test.strftime(cls.txt_datefmt.text()))

    @classmethod
    def edited(cls):
        """Enable the buttons for saving or reverting edits."""
        cls.btn_revert.setEnabled(True)
        cls.btn_save.setEnabled(True)

    @classmethod
    def not_edited(cls):
        """Disable the buttons for saving or reverting edits."""
        cls.btn_revert.setEnabled(False)
        cls.btn_save.setEnabled(False)

    @classmethod
    def refresh(cls):
        """Load and display current settings."""
        # Cancel any scheduled log reloads.
        cls.reload_log = False

        # Load settings into interface.
        cls.txt_logdir.setText(Settings.get_logdir_str())
        cls.txt_logname.setText(Settings.get_logname())
        cls.chk_persist.setChecked(Settings.get_persist())
        cls.txt_datefmt.setText(Settings.get_datefmt())
        cls.chk_decdur.setChecked(Settings.get_decdur())

        # Update interface controls.
        cls.datefmt_edited()
        cls.not_edited()

    @classmethod
    def save(cls):
        """Save the new settings."""
        Settings.set_logdir(cls.txt_logdir.text())
        Settings.set_logname(cls.txt_logname.text())
        Settings.set_persist(cls.chk_persist.isChecked())
        Settings.set_datefmt(cls.txt_datefmt.text())
        Settings.set_decdur(cls.chk_decdur.isChecked())
        cls.not_edited()

        # If we're scheduled to reload the time logs...
        if cls.reload_log:
            # We must do so AFTER updating the path (earlier)
            TimeLog.load(force=True)
            cls.reload_log = False
