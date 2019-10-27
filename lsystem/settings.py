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

