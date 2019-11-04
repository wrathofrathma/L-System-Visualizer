from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
import sys

class gettingStarted(QWidget):
  def __init__(self):
      super().__init__()
      self.initUI()

  def initUI(self):
    self.setWindowTitle('L-system Help')
    self.layout = QGridLayout()
    self.add_labels()
    self.add_widgets()
    self.setLayout(self.layout)

  def add_labels(self):
    self.axiom = QLabel('The axiom is what your string starts as.\n'
                        'Use production rules to transform your axiom.\nSee the symbols glossary for valid inputs.\n')
    self.prodRules = QLabel('Production rules transform your axiom into a string.\n'
                            'The format for production rules is X:Y where X is a symbol in the string and Y is a combination of one or more symbols for X to be replaced with.\n'
                            'For example, an axiom of F with the production rule F: F+F, transforms your axiom into the string F+F.\n')
    self.angle = QLabel('Angle determines how large the turns for + and - are in degrees.\n')
    self.iterations = QLabel('Iterations control how many times production rules are applied to the string.\n'
                             'Going back to the last example, after one iteration F becomes F+F, after two iterations F becomes F+F+F+F, and so on.\n')
    self.turning = QLabel('The Turning Angle determines how large the change in angle is.\n'
                          'This option only appears if there is a ) or ( present in any of your production rules.\n')
    self.scale = QLabel('The Line Scale determines how long or short your line is.\n'
                        'By default, lines are drawn at a unit or half unity length.\n.'
                        'However, if < or > appear in any of your production rules, you can decide how long or short those lines are.\n')
    
  
  def add_widgets(self):
    self.layout.addWidget(self.axiom, 1, 0)
    self.layout.addWidget(self.prodRules, 2, 0)
    self.layout.addWidget(self.angle, 3, 0)
    self.layout.addWidget(self.iterations, 4, 0)
    self.layout.addWidget(self.turning, 5, 0)
    self.layout.addWidget(self.scale, 6, 0)


