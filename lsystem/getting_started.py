from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton
import sys

class GettingStarted(QWidget):
  def __init__(self):
      super().__init__()
      self.init_ui()

  def init_ui(self):
    #sets window title, layout, and adds the widgets to the window
    self.setWindowTitle('L-System Help')
    self.page_one_layout = QGridLayout()
    self.create_widgets()
    self.add_page_one_widgets()
    self.setLayout(self.page_one_layout)

  def create_widgets(self):
    # creates labels and buttons for the window
    self.axiom_one = QLabel('The axiom is where your L-System starts.')
    self.axiom_two = QLabel('Use production rules to transform your axiom into an L-System.')
    self.axiom_three = QLabel('See the symbols glossary for valid inputs.')
    self.next_button = QPushButton("Next Page");
    self.previous_button = QPushButton("Previous Page");
    
  
  def add_page_one_widgets(self):
    # adds widgets to the window
    self.page_one_layout.addWidget(self.axiom_one, 1, 0)
    self.page_one_layout.addWidget(self.axiom_two, 2, 0)
    self.page_one_layout.addWidget(self.axiom_three, 3, 0)
    self.page_one_layout.addWidget(self.next_button, 10, 2, 1, 1)
    self.page_one_layout.addWidget(self.previous_button, 10, 1, 1, 1)
