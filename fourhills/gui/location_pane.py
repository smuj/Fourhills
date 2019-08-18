"""Definition for location pane, listing selectable locations in a region"""


from PySide2 import QtWidgets


class LocationPane(QtWidgets.QWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = QtWidgets.QHBoxLayout()

        self.setLayout(self.layout)
