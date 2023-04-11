"""Edit View [Timecard]
Author(s): Jason C. McDonald

Allows editing a single time log entry.
"""

from datetime import datetime

from PySide6.QtCore import QDate, QDateTime, QTime
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDateTimeEdit,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

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
    spn_hour.setMinimum(0)

    lbl_min = QLabel("Minutes")
    spn_min = QSpinBox()
    spn_min.setMaximum(61)
    spn_min.setMinimum(-1)  # this will get changed to 0 as needed in normalize

    lbl_sec = QLabel("Seconds")
    spn_sec = QSpinBox()
    spn_sec.setMaximum(61)
    spn_sec.setMinimum(-1)  # this will get changed to 0 as needed in normalize

    lbl_activity = QLabel("Activity")
    txt_activity = QLineEdit()

    btn_done = QPushButton(QIcon.fromTheme("cancel"), "Done")
    btn_revert = QPushButton(QIcon.fromTheme("edit-undo"), "Revert")
    btn_save = QPushButton(QIcon.fromTheme("document-save"), "Save")

    index = None
    entry = None

    done_callback = []

    @classmethod
    def build(cls):
        """Build the interface."""

        cls.lbl_timestamp.setWhatsThis("The timestamp for the entry.")
        cls.cal_timestamp.setWhatsThis("The timestamp for the entry.")
        cls.cal_timestamp.setDisplayFormat("yyyy MMM dd hh:mm:ss")
        cls.cal_timestamp.dateTimeChanged.connect(cls.edited)

        cls.lbl_hour.setWhatsThis("The hour part of the entry duration.")
        cls.spn_hour.setWhatsThis("The hour part of the entry duration.")
        cls.spn_hour.valueChanged.connect(cls.edited)

        cls.lbl_min.setWhatsThis("The minute part of the entry duration.")
        cls.spn_min.setWhatsThis("The minute part of the entry duration.")
        cls.spn_min.valueChanged.connect(cls.edited)

        cls.lbl_sec.setWhatsThis("The second part of the entry duration.")
        cls.spn_sec.setWhatsThis("The second part of the entry duration.")
        cls.spn_sec.valueChanged.connect(cls.edited)

        cls.lbl_activity.setWhatsThis("The activity notes for the entry.")
        cls.txt_activity.setWhatsThis("The activity notes for the entry.")
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
    def connect(cls, on_done=None):
        if on_done and on_done not in cls.done_callback:
            cls.done_callback.append(on_done)

    @classmethod
    def done(cls):
        for callback in cls.done_callback:
            callback()

    @classmethod
    def load_item(cls, timestamp):
        cls.entry = TimeLog.retrieve_from_log(timestamp)
        cls.refresh()

    @classmethod
    def normalize(cls):
        # Changes made by normalize should never trigger another event.
        cls.spn_hour.valueChanged.disconnect()
        cls.spn_min.valueChanged.disconnect()
        cls.spn_sec.valueChanged.disconnect()

        hour = cls.spn_hour.value()
        min = cls.spn_min.value()
        sec = cls.spn_sec.value()

        # Handle incrementing rollover of seconds and minutes
        if sec > 59:
            min += sec // 60
            sec %= 60
        if min > 59:
            hour += min // 60
            min %= 60

        # Handle decrementing rollover of seconds and minutes
        if sec < 0 and (hour > 0 or min > 0):
            min -= 1
            sec = 59
        if min < 0 and hour > 0:
            hour -= 1
            min = 59

        # Set the revised values (even if they are the same)
        cls.spn_hour.setValue(hour)
        cls.spn_min.setValue(min)
        cls.spn_sec.setValue(sec)

        # Update the minimums so we never SEE a number lower than 0.
        cls.spn_min.setMinimum(-1 if hour else 0)
        cls.spn_sec.setMinimum(-1 if (min or hour) else 0)

        # Reconnect the signals
        cls.spn_hour.valueChanged.connect(cls.edited)
        cls.spn_min.valueChanged.connect(cls.edited)
        cls.spn_sec.valueChanged.connect(cls.edited)

    @classmethod
    def edited(cls):
        # Normalize times
        cls.normalize()
        # Change interface to allow saving or reverting.
        cls.btn_done.setEnabled(False)
        cls.btn_revert.setEnabled(True)
        cls.btn_save.setEnabled(True)

    @classmethod
    def not_edited(cls):
        cls.btn_done.setEnabled(True)
        cls.btn_revert.setEnabled(False)
        cls.btn_save.setEnabled(False)

    @classmethod
    def refresh(cls):
        if cls.entry is None:
            return
        timestamp = cls.entry.timestamp
        datetime = QDateTime()
        datetime.setDate(QDate(timestamp.year, timestamp.month, timestamp.day))
        datetime.setTime(
            QTime(timestamp.hour, timestamp.minute, timestamp.second)
        )
        cls.cal_timestamp.setDateTime(datetime)

        hours, minutes, seconds = cls.entry.duration
        cls.spn_hour.setValue(hours)
        cls.spn_min.setValue(minutes)
        cls.spn_sec.setValue(seconds)

        cls.txt_activity.setText(cls.entry.notes)

        cls.not_edited()

    @classmethod
    def save(cls):
        TimeLog.remove_from_log(cls.entry.timestamp)
        timestamp = datetime(
            cls.cal_timestamp.date().year(),
            cls.cal_timestamp.date().month(),
            cls.cal_timestamp.date().day(),
            cls.cal_timestamp.time().hour(),
            cls.cal_timestamp.time().minute(),
            cls.cal_timestamp.time().second(),
        )
        new_timestamp = TimeLog.add_to_log(
            timestamp,
            cls.spn_hour.value(),
            cls.spn_min.value(),
            cls.spn_sec.value(),
            cls.txt_activity.text(),
        )
        cls.not_edited()

        cls.entry = TimeLog.retrieve_from_log(new_timestamp)
        # Display the revised data.
        cls.refresh()
