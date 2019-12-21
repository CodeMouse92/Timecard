from PySide2.QtWidgets import QTreeView
from PySide2.QtGui import QStandardItem, QStandardItemModel

from timecard.data.timelog import TimeLog

# Datestamp | Duration | Description


class LogView:
    model = QStandardItemModel(0, 3)
    view = QTreeView()

    @classmethod
    def build(cls):
        """Build the interface"""
        cls.model.setHorizontalHeaderLabels(
            ("Date", "Duration", "Activity")
        )
        # TODO: Lock data types
        cls.view.setModel(cls.model)
        cls.view.setEditTriggers(QTreeView.EditTrigger.DoubleClicked)
        cls.refresh()
        return cls.view

    @classmethod
    def refresh(cls):
        """Reload the data from the log."""
        cls.model.clear()
        # TODO: Implement user settings to format datestamp
        # TODO: Implement user settings to format duration (HMS or decimal)
        for entry in TimeLog.retrieve_log():
            cls.model.appendRow((
                QStandardItem(entry[0]),
                QStandardItem(entry[1]),
                QStandardItem(entry[2])
            ))
