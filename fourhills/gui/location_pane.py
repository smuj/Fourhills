"""Definition for location pane, listing selectable locations in a region"""


from PySide2 import QtWidgets


class LocationPane(QtWidgets.QWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(QtWidgets.QLabel("Location(s):"))
        self.location_list = QtWidgets.QListWidget()
        self.layout.addWidget(self.location_list)

        self.setLayout(self.layout)
