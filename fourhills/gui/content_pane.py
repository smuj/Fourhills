"""Definition for content pane, which contains one or more other panes"""


from PySide2 import QtWidgets
from fourhills.gui.centre_pane import CentrePane
from fourhills.gui.location_pane import LocationPane


class ContentPane(QtWidgets.QWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = QtWidgets.QHBoxLayout()

        # Content pane is initialised with location pane and centre pane
        self.location_pane = LocationPane()
        self.centre_pane = CentrePane()
        self.layout.addWidget(self.location_pane, 1)
        self.layout.addWidget(self.centre_pane, 2)

        self.setLayout(self.layout)
