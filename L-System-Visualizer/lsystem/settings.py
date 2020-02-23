'''This file handles the popup settings window'''
from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QLabel, QButtonGroup, QRadioButton)

from lsystem.LSystemWidget import CameraType

class PopupSettings(QWidget):
    '''This is the window for the popup settings'''
    def __init__(self, graphix):
        '''Initializes important variables for the settings window'''
        super().__init__()
        self.graphix = graphix
        self.dimension = QLabel("Dimensions: ")
        self.two_dim = QRadioButton("2D")
        self.three_dim = QRadioButton("3D")
        self.init_UI()

    def init_UI(self):
        '''Makes the UI for the settings menu'''
        self.setWindowTitle('L-systems Settings')
        self.layout = QGridLayout()
        self.init_buttons()
        self.add_widgets()
        self.setLayout(self.layout)

    def init_buttons(self):
        '''Initializes the buttons and button states in the settings menu'''
        dim_group = QButtonGroup(self)

        if self.graphix.get_camera_type() == 0:
            self.two_dim.setChecked(True)
        self.two_dim.toggled.connect(lambda: self.dim_state(self.two_dim))
        dim_group.addButton(self.two_dim)
        if self.graphix.get_camera_type() == 1:
            self.three_dim.setChecked(True)
        dim_group.addButton(self.three_dim)

    def add_widgets(self):
        '''Adds the widgets to the settings layout'''
        self.layout.addWidget(self.dimension, 1, 0)
        self.layout.addWidget(self.two_dim, 1, 1)
        self.layout.addWidget(self.three_dim, 1, 2)

    def dim_state(self, dim):
        '''Sets the dimension state when changed'''
        if dim.text() == "2D" and dim.isChecked():
            self.graphix.set_camera_type(CameraType.Free)
            self.graphix.set_dimensions(2)
        else:
            self.graphix.set_dimensions(3)
            self.graphix.set_camera_type(CameraType.Orbital)
