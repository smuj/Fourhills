"""Definition for location pane, listing selectable locations in a region"""

import os
from PySide2 import QtWidgets

from fourhills.fourhills import SCENE_FILENAME


class LocationPane(QtWidgets.QWidget):

    def __init__(self, setting, **kwargs):
        super().__init__(**kwargs)
        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(QtWidgets.QLabel("Location(s):"))
        self.location_list = QtWidgets.QListWidget()
        self.layout.addWidget(self.location_list)

        self.setLayout(self.layout)

        self.setting = setting
        self.populate_locations()

    def populate_locations(self):
        """Search for folders with scene file and make them available as locations"""
        self.location_list.clear()
        world_dir = self.setting.world_dir
        for root, dirs, files in os.walk(world_dir):
            if SCENE_FILENAME in files:
                rel_path = os.path.relpath(root, world_dir)
                rel_path.replace(os.path.sep, "/")
                self.location_list.addItem(rel_path)
