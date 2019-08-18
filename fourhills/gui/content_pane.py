"""Definition for content pane, which contains one or more other panes"""


from PySide2 import QtWidgets


class ContentPane(QtWidgets.QWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = QtWidgets.QHBoxLayout()

        self.setLayout(self.layout)
