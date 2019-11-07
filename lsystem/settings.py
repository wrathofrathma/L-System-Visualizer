from PyQt5.QtWidgets import QRadioButton, QButtonGroup, QMainWindow, QPushButton, QWidget, QLineEdit, QTextEdit, QGridLayout, QApplication, QLabel
import sys
from PyQt5 import QtWidgets, QtCore
import numpy as np
from math import pi
from lsystem.LSystemWidget import *
from lsystem.lsystem_utils import *

class PopupSettings(QWidget):
  def __init__(self, graphix):
      super().__init__()
      self.graphix = graphix
      self.initUI()


  def initUI(self):
    self.setWindowTitle('L-systems Settings')
    self.layout = QGridLayout()
    self.init_text_boxes()
    self.init_buttons()
    self.add_widgets()
    self.setLayout(self.layout)

  def init_text_boxes(self):
    self.dimension = QLabel("Dimensions: ")
    self.color = QLabel("Color: ")
    self.feature = QLabel("Feature: ")

  def init_buttons(self):
    dim_group = QButtonGroup(self)
    color_group = QButtonGroup(self)
    feature_group = QButtonGroup(self)

    self.two_dim = QRadioButton("2D")
    if self.graphix.get_camera_type() == 0:
      self.two_dim.setChecked(True)
    self.two_dim.toggled.connect(lambda: self.dim_state(self.two_dim))
    dim_group.addButton(self.two_dim)
    self.three_dim = QRadioButton("3D")
    if self.graphix.get_camera_type() == 1:
      self.three_dim.setChecked(True)
    dim_group.addButton(self.three_dim)

    is_colorful, is_flashing = self.graphix.get_mesh_options()

    self.white = QRadioButton("White")
    if not is_colorful:
      self.white.setChecked(True)
    self.white.toggled.connect(lambda: self.color_state(self.white))
    color_group.addButton(self.white)
    self.rainbow = QRadioButton("Rainbow")
    self.rainbow.toggled.connect(lambda: self.color_state(self.rainbow))
    if is_colorful:
      self.rainbow.setChecked(True)
    color_group.addButton(self.rainbow)

    self.none = QRadioButton("None")
    if not is_flashing:
      self.none.setChecked(True)
    self.none.toggled.connect(lambda: self.feature_state(self.none))
    feature_group.addButton(self.none)
    self.flashing = QRadioButton('Flashing')
    self.flashing.toggled.connect(lambda: self.feature_state(self.flashing))
    if is_flashing:
      self.flashing.setChecked(True)
    feature_group.addButton(self.flashing)


  def add_widgets(self):
    self.layout.addWidget(self.dimension, 1, 0)
    self.layout.addWidget(self.color, 2, 0)
    self.layout.addWidget(self.feature, 3, 0)
    self.layout.addWidget(self.two_dim, 1, 1)
    self.layout.addWidget(self.three_dim, 1, 2)
    self.layout.addWidget(self.white, 2, 1)
    self.layout.addWidget(self.rainbow, 2, 2)
    self.layout.addWidget(self.none, 3, 1)
    self.layout.addWidget(self.flashing, 3, 2)

  def dim_state(self, dim):
    if dim.text() == "2D" and dim.isChecked():
        self.graphix.set_camera_type(CameraType.Free)
    else:
        self.graphix.set_camera_type(CameraType.Orbital)

  def color_state(self, color):
    if color.text() == 'White' and color.isChecked():
      self.graphix.set_mesh_options(MeshOptions.White)
    elif color.text() == "Rainbow" and color.isChecked():
      self.graphix.set_mesh_options(MeshOptions.Colors)

  def feature_state(self, feature):
    if feature.text() == 'None' and feature.isChecked():
      self.graphix.set_mesh_options(MeshOptions.Static)
    elif feature.text() == 'Flashing' and feature.isChecked():
      self.graphix.set_mesh_options(MeshOptions.Pulse)
