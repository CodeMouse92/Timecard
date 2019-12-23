from PySide2.QtWidgets import QWidget, QTreeWidget, QGridLayout, QPushButton
from PySide2.QtWidgets import QTreeWidgetItem
from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtGui import QIcon

from timecard.data.timelog import TimeLog

# Datestamp | Duration | Description


class LogView:
    widget = QWidget()
    layout = QGridLayout()
    tree_log = QTreeWidget()

    btn_edit = QPushButton()
    btn_delete = QPushButton()

    edit_callback = None

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
            item.setText(0, entry.timestamp_as_format("%m/%d/%y %H:%M:%S"))
            item.setText(1, entry.duration_as_string())
            item.setText(2, entry.notes)
            item.setToolTip(0, item.text(0))
            item.setToolTip(1, item.text(1))
            item.setToolTip(2, item.text(2))
            cls.tree_log.addTopLevelItem(item)

    @classmethod
    def connect(cls, /, edit=None):
        if edit:
            cls.edit_callback = edit

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
    def _selected_index(cls):
        item = cls.tree_log.selectedItems()[0]
        return cls.tree_log.indexFromItem(item).row()

    @classmethod
    def delete(cls):
        index = cls._selected_index()
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
        index = cls._selected_index()
        if cls.edit_callback:
            cls.edit_callback(index)
