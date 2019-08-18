"""Define a Qt Widget for the Notes Pane"""

from PySide2 import QtWidgets


class NotesPane(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = QtWidgets.QVBoxLayout()

        # Add file information
        self.file_layout = QtWidgets.QHBoxLayout()
        self.load_btn = QtWidgets.QPushButton("Load File")
        self.save_btn = QtWidgets.QPushButton("Save File")
        self.file_path = QtWidgets.QLineEdit("<none>")
        self.file_path.setReadOnly(True)
        self.file_layout.addWidget(self.load_btn)
        self.file_layout.addWidget(self.save_btn)
        self.file_layout.addWidget(self.file_path)
        self.layout.addLayout(self.file_layout)

        # Add notes text box
        self.notes_text = QtWidgets.QTextEdit()
        self.layout.addWidget(self.notes_text)

        self.setLayout(self.layout)
