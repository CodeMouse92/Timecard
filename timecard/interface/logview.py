from PySide2.QtWidgets import QTreeView
from PySide2.QtGui import QStandardItemModel


# Datestamp | Description | Duration

class LogView:
    model = QStandardItemModel(1, 3)
    view = QTreeView()

    @classmethod
    def build(cls):
        cls.model.setHorizontalHeaderLabels(
            ("Date", "Activity", "Duration")
        )
        # TODO: Lock data types
        cls.view.setModel(cls.model)
        cls.view.setEditTriggers(QTreeView.EditTrigger.DoubleClicked)
        return cls.view
