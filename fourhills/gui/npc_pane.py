"""Definition for NPC pane, which shows information about NPCs at a location"""


from PySide2 import QtWidgets


class NpcPane(QtWidgets.QWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = QtWidgets.QHBoxLayout()

        self.setLayout(self.layout)
