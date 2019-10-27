from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QLineEdit, QTextEdit, QGridLayout, QApplication, QLabel
import sys
from PyQt5 import QtWidgets, QtCore
import numpy as np
from math import pi
from lsystem.LSystemWidget import *
from lsystem.lsystem_utils import *

class PopupSettings(QWidget):
  def __init__(self):
      super().__init__()
      self.initUI()

  def initUI(self):
    self.setWindowTitle('L-systems Settings')
    self.layout = QGridLayout()
    self.init_text_boxes()
    self.add_widgets()

  def init_text_boxes():
    self.dimension = QLabel("Dimensions: ")
    self.color = QLabel("Color: ")
    self.flashing = QLabel("Flashing: ")
  
  def add_widgets():
    self.layout.addWidget(self.dimension, 1, 0)
    self.layout.addWidget(self.color, 2, 0)
    self.layout.addWidget(self.flashing, 3, 0)

