from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
from lsystem.lsystem_utils import save_lsystem
import sys
import os

class ScreenshotWindow(QWidget):
  def __init__(self, ui):
      super().__init__()
      self.ui = ui
      self.init_ui()

  def init_ui(self):
    #sets the window title, layout, and adds widgets to the window
    self.setWindowTitle('Take a screenshot')
    self.layout = QGridLayout()
    self.create_widgets()
    self.add_widgets()
    self.setLayout(self.layout)

  def create_widgets(self):
    #creates the widgets to be added to the window
    self.save_label = QLabel('Name your file without a file extension')
    self.name_box = QLineEdit()
    self.name_box.returnPressed.connect(lambda: self.save())
    self.save_button = QPushButton('Save your screenshot')
    self.save_button.clicked.connect(lambda: self.save())
  
  def add_widgets(self):
    #adds the widgets to the window
    self.layout.addWidget(self.save_label, 1, 0)
    self.layout.addWidget(self.name_box, 1, 1,1,2)
    self.layout.addWidget(self.save_button, 1, 3)

  def save(self):
    #grabs the name of the lsystem from the namebox, grabs the grammar from the ui, and calls save_lsystem in lsystem_utils.py
    name = self.name_box.text()
    if len(name) > 0:
      if not os.path.isdir('screenshots/'):
        os.mkdir('screenshots/')
      self.ui.graphix.screenshot("screenshots/" + name + ".png")
      print("[ INFO ] L-System " + str(name) + " saved to disk...")
      #make window disappear
      self.hide()
      return name
    else:
      self.name_box.setStyleSheet("color: red;")
      self.name_box.setText("Name your L-System before you save!")
