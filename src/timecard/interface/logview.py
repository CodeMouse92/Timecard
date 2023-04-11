"""Log View [Timecard]
Author(s): Jason C. McDonald

Displays the current log entries and allows deleting or triggering edits
on them.
"""

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QGridLayout,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
)

from timecard.data.settings import Settings
from timecard.data.timelog import TimeLog

# Datestamp | Duration | Description


class LogViewEntry(QTreeWidgetItem):
    def __init__(self, entry, *args, **kwargs):
        self.entry = entry
        super().__init__(*args, **kwargs)

        self.setText(0, self.entry.timestamp_as_format(Settings.get_datefmt()))
        self.setText(1, self.entry.duration_as_string(Settings.get_decdur()))
        self.setText(2, self.entry.notes)
        self.setToolTip(0, self.text(0))
        self.setToolTip(1, self.text(1))
        self.setToolTip(2, self.text(2))

    def get_timestamp(self):
        return self.entry.timestamp


class LogView:
    widget = QWidget()
    layout = QGridLayout()
    tree_log = QTreeWidget()

    btn_edit = QPushButton()
    btn_delete = QPushButton()

    edit_callback = []

    @classmethod
    def build(cls):
        """Build the interface"""
        cls.tree_log.setWhatsThis("The time log.")
        cls.tree_log.setHeaderLabels(["Date", "Duration", "Activity"])
        cls.tree_log.setSortingEnabled(True)
        cls.layout.addWidget(cls.tree_log, 0, 0, 3, 3)
        cls.refresh()

        cls.layout.addWidget(cls.btn_delete, 3, 1, 1, 1)
        cls.layout.addWidget(cls.btn_edit, 3, 2, 1, 1)
        cls.unselected()
        cls._set_mode_default()

        cls.tree_log.itemClicked.connect(cls.selected)

        cls.widget.setLayout(cls.layout)
        return cls.widget

    @classmethod
    def refresh(cls):
        """Reload the data from the log."""
        cls.tree_log.clear()
        for entry in TimeLog.retrieve_log():
            item = LogViewEntry(entry)
            cls.tree_log.addTopLevelItem(item)

    @classmethod
    def connect(cls, on_edit=None):
        if on_edit and on_edit not in cls.edit_callback:
            cls.edit_callback.append(on_edit)

    @classmethod
    def _disconnect_buttons(cls):
        """Disconnect signals from the control buttons.
        This must be done before new signals can be added properly.
        """
        try:
            cls.btn_edit.clicked.disconnect()
        except RuntimeError:
            pass

        try:
            cls.btn_delete.clicked.disconnect()
        except RuntimeError:
            pass

    @classmethod
    def _set_mode_default(cls):
        cls._disconnect_buttons()

        cls.btn_delete.setText("Delete")
        cls.btn_delete.setIcon(QIcon.fromTheme("edit-delete"))
        cls.btn_delete.setWhatsThis("Delete the selected log entry.")
        cls.btn_delete.clicked.connect(cls.prompt_delete)

        cls.btn_edit.setText("Edit")
        cls.btn_edit.setIcon(QIcon.fromTheme("document-properties"))
        cls.btn_edit.setWhatsThis("Edit the selected log entry.")
        cls.btn_edit.clicked.connect(cls.edit)

    @classmethod
    def _set_mode_prompt_delete(cls):
        cls._disconnect_buttons()

        cls.btn_delete.setText("Confirm Delete")
        cls.btn_delete.setIcon(QIcon.fromTheme("edit-delete"))
        cls.btn_delete.setWhatsThis("Delete the selected log entry.")
        cls.btn_delete.clicked.connect(cls.delete)

        cls.btn_edit.setText("Keep")
        cls.btn_edit.setIcon(QIcon.fromTheme("edit-undo"))
        cls.btn_edit.setWhatsThis("Keep the selected log entry.")
        cls.btn_edit.clicked.connect(cls.cancel)

    @classmethod
    def _selected_entry(cls):
        item = cls.tree_log.selectedItems()[0]
        return item.get_timestamp()

    @classmethod
    def delete(cls):
        timestamp = cls._selected_entry()
        TimeLog.remove_from_log(timestamp)
        cls.refresh()

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
        timestamp = cls._selected_entry()
        for callback in cls.edit_callback:
            callback(timestamp)
