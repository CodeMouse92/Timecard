from PySide2.QtWidgets import QWidget, QTreeWidget, QGridLayout, QPushButton, QTreeWidgetItem
from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtGui import QIcon

from timecard.data.timelog import TimeLog

# Datestamp | Duration | Description


class LogView:
    widget = QWidget()
    layout = QGridLayout()
    #model = QStandardItemModel(0, 3)
    tree_log = QTreeWidget()

    btn_delete = QPushButton()

    @classmethod
    def build(cls):
        """Build the interface"""
        # TODO: Lock data types?
        cls.tree_log.setWhatsThis("The time log.")
        cls.layout.addWidget(cls.tree_log, 0, 0, 3, 3)
        cls.refresh()

        cls.layout.addWidget(cls.btn_delete, 3, 2, 1, 1)
        cls._set_mode_default()

        cls.tree_log.itemClicked.connect(cls.selected)

        cls.widget.setLayout(cls.layout)
        return cls.widget

    # TODO: Add sorting by column

    @classmethod
    def refresh(cls):
        """Reload the data from the log."""
        #cls.model.clear()
        cls.tree_log.clear()
        cls.tree_log.setHeaderLabels(
            ["Date", "Duration", "Activity"]
        )
        # TODO: Implement user settings to format datestamp
        # TODO: Implement user settings to format duration (HMS or decimal)
        for entry in TimeLog.retrieve_log():
            item = QTreeWidgetItem()
            item.setText(0, entry[0])
            item.setText(1, entry[1])
            item.setText(2, entry[2])
            cls.tree_log.addTopLevelItem(item)

    @classmethod
    def _disconnect_buttons(cls):
        """Disconnect signals from the control buttons.
        This must be done before new signals can be added properly.
        """
        try:
            cls.btn_delete.clicked.disconnect()
        except RuntimeError:
            pass

    @classmethod
    def _set_mode_default(cls):
        cls._disconnect_buttons()

        cls.btn_delete.setText("Delete")
        cls.btn_delete.setIcon(QIcon.fromTheme('edit-delete'))
        cls.btn_delete.clicked.connect(cls.prompt_delete)
        cls.unselected()

    @classmethod
    def _set_mode_prompt_delete(cls):
        cls._disconnect_buttons()

        cls.btn_delete.setText("Confirm Delete")
        cls.btn_delete.setIcon(QIcon.fromTheme('edit-delete'))
        cls.btn_delete.clicked.connect(cls.delete)

    @classmethod
    def delete(cls):
        for item in cls.tree_log.selectedItems():
            index = cls.tree_log.indexFromItem(item).row()
            cls.tree_log.takeTopLevelItem(index)
            TimeLog.remove_from_log(index)

        # We must set to default AFTER, lest our selection get unselected
        cls._set_mode_default()

    @classmethod
    def prompt_delete(cls):
        cls._set_mode_prompt_delete()

    @classmethod
    def unselected(cls):
        cls.tree_log.clearSelection()
        cls.btn_delete.setEnabled(False)

    @classmethod
    def selected(cls):
        cls.btn_delete.setEnabled(True)
