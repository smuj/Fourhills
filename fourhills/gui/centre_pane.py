"""
Definition for centre pane, which shows various kinds of information such as scene information,
battle information, and will be updated to contain other kinds.
"""


from PySide2 import QtWidgets


class CentrePane(QtWidgets.QWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = QtWidgets.QHBoxLayout()

        self.setLayout(self.layout)
