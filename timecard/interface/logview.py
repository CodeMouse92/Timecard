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

    btn_edit = QPushButton()
    btn_delete = QPushButton()

    @classmethod
    def build(cls):
        """Build the interface"""
        cls.tree_log.setWhatsThis("The time log.")
        cls.tree_log.setSortingEnabled(True)
        cls.layout.addWidget(cls.tree_log, 0, 0, 3, 3)
        cls.refresh()

        cls.layout.addWidget(cls.btn_edit, 3, 1, 1, 1)
        cls.layout.addWidget(cls.btn_delete, 3, 2, 1, 1)
        cls.unselected()
        cls._set_mode_default()

        cls.tree_log.itemClicked.connect(cls.selected)

        cls.widget.setLayout(cls.layout)
        return cls.widget

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
            item.setToolTip(0, entry[0])
            item.setToolTip(1, entry[1])
            item.setToolTip(2, entry[2])
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

        cls.btn_edit.setText("Edit")
        cls.btn_edit.setIcon(QIcon.fromTheme('document-properties'))
        cls.btn_edit.clicked.connect(cls.edit)

        cls.btn_delete.setText("Delete")
        cls.btn_delete.setIcon(QIcon.fromTheme('edit-delete'))
        cls.btn_delete.clicked.connect(cls.prompt_delete)

    @classmethod
    def _set_mode_prompt_delete(cls):
        cls._disconnect_buttons()

        cls.btn_edit.setText("Cancel")
        cls.btn_edit.setIcon(QIcon.fromTheme('cancel'))
        cls.btn_edit.clicked.connect(cls.cancel)

        cls.btn_delete.setText("Confirm Delete")
        cls.btn_delete.setIcon(QIcon.fromTheme('edit-delete'))
        cls.btn_delete.clicked.connect(cls.delete)

    @classmethod
    def delete(cls):
        for item in cls.tree_log.selectedItems():
            index = cls.tree_log.indexFromItem(item).row()
            cls.tree_log.takeTopLevelItem(index)
            TimeLog.remove_from_log(index)

        cls.unselected()
        cls._set_mode_default()

    @classmethod
    def cancel(cls):
        cls._set_mode_default()

    @classmethod
    def prompt_delete(cls):
        cls._set_mode_prompt_delete()

    @classmethod
    def unselected(cls):
        cls.tree_log.clearSelection()
        cls.btn_edit.setEnabled(False)
        cls.btn_delete.setEnabled(False)

    @classmethod
    def selected(cls):
        cls.btn_edit.setEnabled(True)
        cls.btn_delete.setEnabled(True)
        cls._set_mode_default()

    @classmethod
    def edit(cls):
        # TODO: Add EditView (switch on Workspace).
        # EditView will allows editing item correctly, respecting data types.
        pass
