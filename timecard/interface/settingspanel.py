from PySide2.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout
from PySide2.QtWidgets import QLabel, QCheckBox, QLineEdit, QPushButton
from PySide2.QtGui import QIcon

from timecard.data.settings import Settings


class SettingsPanel:
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
    chk_pomodoro = QCheckBox("Use Pomodoro")

    btn_revert = QPushButton(QIcon.fromTheme('edit-undo'), "Revert")
    btn_save = QPushButton(QIcon.fromTheme('document-save'), "Save")

    @classmethod
    def build(cls):
        """Build the interface."""
        cls.txt_logdir.textEdited.connect(cls.edited)
        cls.txt_logname.textEdited.connect(cls.edited)
        cls.chk_pomodoro.stateChanged.connect(cls.edited)

        cls.grid_layout.addWidget(cls.lbl_logdir, 0, 0)
        cls.grid_layout.addWidget(cls.txt_logdir, 0, 1)
        cls.grid_layout.addWidget(cls.lbl_logname, 1, 0)
        cls.grid_layout.addWidget(cls.txt_logname, 1, 1)
        cls.grid_layout.addWidget(cls.chk_pomodoro, 2, 1)
        cls.grid_widget.setLayout(cls.grid_layout)

        cls.buttons_layout.addWidget(cls.btn_revert)
        cls.buttons_layout.addWidget(cls.btn_save)
        cls.btn_save.clicked.connect(cls.save)
        cls.btn_revert.clicked.connect(cls.refresh)

        cls.buttons_widget.setLayout(cls.buttons_layout)
        cls.layout.addWidget(cls.grid_widget)
        cls.layout.addWidget(cls.buttons_widget)
        cls.widget.setLayout(cls.layout)

        cls.refresh()
        return cls.widget

    @classmethod
    def edited(cls):
        cls.btn_revert.setEnabled(True)
        cls.btn_save.setEnabled(True)

    @classmethod
    def not_edited(cls):
        cls.btn_revert.setEnabled(False)
        cls.btn_save.setEnabled(False)

    @classmethod
    def refresh(cls):
        cls.txt_logdir.setText(Settings.get_logdir_str())
        cls.txt_logname.setText(Settings.get_logname())
        cls.not_edited()

    @classmethod
    def save(cls):
        Settings.set_logdir(cls.txt_logdir.text())
        Settings.set_logname(cls.txt_logname.text())
        cls.not_edited()
