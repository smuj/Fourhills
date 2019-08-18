"""Definition for monsters pane, showing information about monsters at a location"""


from PySide2 import QtWidgets


class MonsterPane(QtWidgets.QWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = QtWidgets.QHBoxLayout()

        self.setLayout(self.layout)
