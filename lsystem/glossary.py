from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
import sys

class Glossary(QWidget):
  def __init__(self):
      super().__init__()
      self.initUI()

  def initUI(self):
    self.setWindowTitle('Symbol Glossary')
    self.layout = QGridLayout()
    self.add_labels()
    self.add_widgets()
    self.setLayout(self.layout)

  def add_labels(self):
    self.bigF = QLabel('F: draws a line of unit length.')
    self.littleF = QLabel('f: Moves forward in a line of unit length.')
    self.bigG = QLabel('G: draws a line of unit length.')
    self.littleG = QLabel('g: moves forward in a line of unit length.')
    self.bigH = QLabel('H: draws a line of half unit length.')
    self.littleH = QLabel('h: moves forward in a line of half unit length.')
    self.plus = QLabel('+: turns the angle counter-clockwise by an angle.')
    self.minus = QLabel('-: turns the angle clockwise by an angle.')
    self.pipe = QLabel('|: reverses direction.')
    self.leftBracket = QLabel('[: starts a branch. Must have a ] somewhere after.')
    self.rightBracket = QLabel(']: ends a branch. Must have a [ somewhere before.')
    self.leftParenthesis = QLabel('(: decreases the angle by a turning angle.')
    self.rightParenthesis = QLabel('): increses the angle by a turning angle.')
    self.leftAngle = QLabel('<: divides line length by the length factor.')
    self.rightAngle = QLabel('>: multiplies the line length by the length factor.')
    self.control = QLabel('A-E, I-Z: Control characters to control how the curve advances')

  
  def add_widgets(self):
    self.layout.addWidget(self.bigF, 1, 0)
    self.layout.addWidget(self.littleF, 2, 0)
    self.layout.addWidget(self.bigG, 3, 0)
    self.layout.addWidget(self.littleG, 4, 0)
    self.layout.addWidget(self.bigH, 5, 0)
    self.layout.addWidget(self.littleH, 6, 0)
    self.layout.addWidget(self.plus, 7, 0)
    self.layout.addWidget(self.minus, 8, 0)
    self.layout.addWidget(self.leftBracket, 9, 0)
    self.layout.addWidget(self.rightBracket, 10, 0)
    self.layout.addWidget(self.leftParenthesis, 11, 0)
    self.layout.addWidget(self.rightParenthesis, 12, 0)
    self.layout.addWidget(self.leftAngle, 13, 0)
    self.layout.addWidget(self.rightAngle, 14, 0)
    self.layout.addWidget(self.control, 15, 0)


