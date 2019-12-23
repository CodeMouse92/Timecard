from PySide2.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QLabel, QLineEdit, QDateTimeEdit, QSpinBox
from PySide2.QtGui import QIcon
from PySide2.QtCore import QDateTime, QDate, QTime

from timecard.data.timelog import TimeLog


class EditView:
    widget = QWidget()
    layout = QVBoxLayout()
    grid_widget = QWidget()
    grid_layout = QGridLayout()
    buttons_widget = QWidget()
    buttons_layout = QHBoxLayout()

    lbl_timestamp = QLabel("Timestamp")
    cal_timestamp = QDateTimeEdit()
    lbl_duration = QLabel("Duration")
    lbl_hour = QLabel("Hours")
    spn_hour = QSpinBox()
    lbl_min = QLabel("Minutes")
    spn_min = QSpinBox()
    lbl_sec = QLabel("Seconds")
    spn_sec = QSpinBox()
    lbl_activity = QLabel("Activity")
    txt_activity = QLineEdit()

    btn_done = QPushButton(QIcon.fromTheme('cancel'), "Done")
    btn_revert = QPushButton(QIcon.fromTheme('edit-undo'), "Revert")
    btn_save = QPushButton(QIcon.fromTheme('document-save'), "Save")

    index = None
    entry = None

    done_callback = None

    @classmethod
    def build(cls):
        """Build the interface."""

        cls.cal_timestamp.dateTimeChanged.connect(cls.edited)
        cls.spn_hour.valueChanged.connect(cls.edited)
        cls.spn_min.valueChanged.connect(cls.edited)
        cls.spn_sec.valueChanged.connect(cls.edited)
        cls.txt_activity.textChanged.connect(cls.edited)

        cls.grid_layout.addWidget(cls.lbl_timestamp, 0, 0, 1, 1)
        cls.grid_layout.addWidget(cls.cal_timestamp, 0, 1, 1, 1)

        cls.grid_layout.addWidget(cls.lbl_duration, 2, 0, 1, 2)
        cls.grid_layout.addWidget(cls.lbl_hour, 3, 0, 1, 1)
        cls.grid_layout.addWidget(cls.spn_hour, 3, 1, 1, 1)
        cls.grid_layout.addWidget(cls.lbl_min, 4, 0, 1, 1)
        cls.grid_layout.addWidget(cls.spn_min, 4, 1, 1, 1)
        cls.grid_layout.addWidget(cls.lbl_sec, 5, 0, 1, 1)
        cls.grid_layout.addWidget(cls.spn_sec, 5, 1, 1, 1)

        cls.grid_layout.addWidget(cls.lbl_activity, 6, 0, 1, 1)
        cls.grid_layout.addWidget(cls.txt_activity, 6, 1, 1, 1)

        cls.grid_widget.setLayout(cls.grid_layout)

        cls.btn_done.clicked.connect(cls.done)
        cls.btn_done.setWhatsThis("Return to time log.")
        cls.buttons_layout.addWidget(cls.btn_done)
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
    def connect(cls, /, done=None):
        if done:
            cls.done_callback = done

    @classmethod
    def done(cls):
        if cls.done_callback:
            cls.done_callback()

    @classmethod
    def load_item(cls, index):
        cls.index = index
        cls.entry = TimeLog.retrieve_from_log(cls.index)
        cls.refresh()

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
        if cls.entry is None:
            return
        timestamp = cls.entry.timestamp
        datetime = QDateTime()
        datetime.setDate(QDate(timestamp.year,
                               timestamp.month,
                               timestamp.day))
        datetime.setTime(QTime(timestamp.hour,
                               timestamp.minute,
                               timestamp.second))
        cls.cal_timestamp.setDateTime(datetime)

        hours, minutes, seconds = cls.entry.duration
        cls.spn_hour.setValue(hours)
        cls.spn_min.setValue(minutes)
        cls.spn_sec.setValue(seconds)

        cls.txt_activity.setText(cls.entry.notes)

        cls.not_edited()

    @classmethod
    def save(cls):
        timestamp = (f"{cls.cal_timestamp.date().year()}-"
                     f"{cls.cal_timestamp.date().month()}-"
                     f"{cls.cal_timestamp.date().day()}-"
                     f"{cls.cal_timestamp.time().hour()}-"
                     f"{cls.cal_timestamp.time().minute()}-"
                     f"{cls.cal_timestamp.time().second()}"
                     )
        TimeLog.edit_in_log(cls.index,
                            timestamp,
                            cls.spn_hour.value(),
                            cls.spn_min.value(),
                            cls.spn_sec.value(),
                            cls.txt_activity.text()
                            )
        cls.not_edited()
