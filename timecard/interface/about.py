from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QVBoxLayout, QTextEdit


class About:
    widget = QWidget()
    layout = QVBoxLayout()
    lbl_info = QTextEdit()

    @classmethod
    def build(cls):
        """Build the interface."""
        cls.lbl_info = QTextEdit()
        cls.lbl_info.setPlainText("Timecard 2.0\n"
                                  "Created By Jason C. McDonald (CodeMouse92)\n"
                                  "https://github.com/codemouse92/timecard\n"
                                  )
        cls.lbl_info.setReadOnly(True)
        cls.lbl_info.setAlignment(Qt.AlignCenter)

        cls.widget.setLayout(cls.layout)
        cls.layout.addWidget(cls.lbl_info)

        return cls.widget
