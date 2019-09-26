from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QLineEdit, QTextEdit, QGridLayout, QApplication, QLabel
import sys
from PyQt5 import QtWidgets, QtCore
from LSystemWidget import *
import numpy as np
from Lsystem import *
from stack_loop import *
from math import pi

alphabet = ["F","f","-","+"]
error_message = "X"
class CustomLineEdit(QtWidgets.QLineEdit):
    clicked = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()
    def clear_box(self):
      if self.text() == error_message:
        self.setText('')
        self.setStyleSheet("color: black;")
class UIWidget(QWidget):

  def __init__(self):
    super(UIWidget, self).__init__()
    self.initUI()
    self.graphix = LSystemDisplayWidget()
    self.graphix.show()
  def initUI(self):

    #renames the window
    self.setWindowTitle('L-Systems Generator')

    #creates the labels for each text box
    self.axiom = QLabel('Axiom')
    self.prodrules = QLabel('Production Rules')
    self.angle = QLabel('Angles(degrees)')
    self.iters = QLabel('Iterations')

    """
    #creates the text box for each label
    self.axiomEdit = QLineEdit()
    self.axiomEdit.clicked.connect(self.clearBox(self.axiomEdit))
    self.prodrulesEdit = QLineEdit()
    self.angleEdit = QLineEdit()
    self.itersEdit = QLineEdit()
    """
     #creates the text box for each label
    self.axiomEdit = CustomLineEdit()
    self.axiomEdit.clicked.connect(lambda: self.axiomEdit.clear_box())
    self.prodrulesEdit = CustomLineEdit()
    self.prodrulesEdit.clicked.connect(lambda: self.prodrulesEdit.clear_box())
    self.angleEdit = CustomLineEdit()
    self.angleEdit.clicked.connect(lambda: self.angleEdit.clear_box())
    self.itersEdit = CustomLineEdit()
    self.itersEdit.clicked.connect(lambda: self.itersEdit.clear_box())

    #creates a grid for the layout
    grid = QGridLayout()
    grid.setSpacing(20)

    #adds the labels and textboxes into the grid
    grid.addWidget(self.axiom, 1, 0)
    grid.addWidget(self.axiomEdit, 1, 1)

    grid.addWidget(self.prodrules, 2, 0)
    grid.addWidget(self.prodrulesEdit, 2, 1)

    grid.addWidget(self.angle, 3, 0)
    grid.addWidget(self.angleEdit, 3, 1)

    grid.addWidget(self.iters, 4, 0)
    grid.addWidget(self.itersEdit, 4, 1)

    #makes the lsys generator button
    lsysbutton = QPushButton("Generate L System", self)
    grid.addWidget(lsysbutton, 8, 0)
    lsysbutton.clicked.connect(self.genLSys)

    #make the exit button
    exitbutton = QPushButton("Exit", self)
    grid.addWidget(exitbutton, 8, 1)
    exitbutton.clicked.connect(exit)

    #loads the grid into the layout
    self.setLayout(grid)

  def inputCheck(self):
    valid_input = 1
    axiomInput = self.axiomEdit.text()
    prodInput = self.prodrulesEdit.text()
    angleInput = self.angleEdit.text()
    itersInput = self.itersEdit.text()
    string = 0
    for ch in axiomInput:
      if not axiomInput in alphabet:
        self.axiomEdit.setStyleSheet("color: red;")
        self.axiomEdit.setText(error_message)
        valid_input = 0
    prodInput=prodInput.replace(' ','')
    if not '->' in prodInput or prodInput[1]=='>' or prodInput[len(prodInput)-1]=='>':
      self.prodrulesEdit.setStyleSheet("color: red;")
      self.prodrulesEdit.setText(error_message)
      valid_input = 0
    tmp_prodRule = prodInput.replace('->','')
    for ch in tmp_prodRule:
      if not ch in alphabet:
        self.prodrulesEdit.setStyleSheet("color: red;")
        self.prodrulesEdit.setText(error_message)
        valid_input = 0

    try:
      angleInput = float(angleInput)
    except:
      self.angleEdit.setStyleSheet("color: red;")
      self.angleEdit.setText("X")
      valid_input=0
      string = 1 #is a string
    if not string:
      if angleInput <= -360 or angleInput >= 360:
        self.angleEdit.setStyleSheet("color: red;")
        self.angleEdit.setText(error_message)
        valid_input = 0

    try:
      itersInput = int(itersInput)
    except:
      self.itersEdit.setStyleSheet("color: red;")
      self.itersEdit.setText(error_message)
      valid_input = 0
      string = 1 #is a string
    if not string:
      if itersInput <= 0:
        self.itersEdit.setStyleSheet("color: red;")
        self.itersEdit.setText(error_message)
        valid_input = 0
    return valid_input

  #Probably doesn't need self as a param, can just be static.
  # Generates a rule dictionary from an array of production rule strings taken from the UI
  def genRuleDict(self, prodRules):
      rules = {}
      for rule in prodRules:
          pr = rule.replace("->"," ")
          pr = pr.split(' ')
          rules[pr[0]]=pr[1]
      return rules

  def genLSys(self):
    if self.inputCheck():
      axiomInput = self.axiomEdit.text()
      prodInput = [self.prodrulesEdit.text()] #changed to array
      angleInput = self.angleEdit.text()
      itersInput = self.itersEdit.text()
      print("Axiom: ", axiomInput)
      print("Productions: ")
      for prod in prodInput:
          print(prod)
      print("Angle: ", angleInput)
      print("Iterations: ", itersInput)
      # Format input for use
      rules=self.genRuleDict(prodInput)
      angle = float(angleInput)
      angle = angle*pi/180.0 # degrees to radians
      it = int(itersInput)
      # Generates full production string
      s = lgen(axiomInput, rules, it)
      print(s)
      # Generates vertices
      verts = readStack(s,(0,0),angle)
      # Converts to usable normalized coordinates
      verts = np.array(verts, dtype=np.float32)
      verts = verts.reshape(verts.shape[0],verts.shape[1])
      verts = normalize_coordinates(verts)
      print(verts)
      # Sets verts on graphics widget and draws
      self.graphix.add_vertices(verts)
      self.graphix.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UIWidget()
    ui.show()

    sys.exit(app.exec_())
