from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QLineEdit, QTextEdit, QGridLayout, QApplication, QLabel
import sys
from PyQt5 import QtWidgets, QtCore
import numpy as np
from math import pi
from lsystem.LSystemWidget import *
from lsystem.lsystem_utils import *


alphabet = ["F","f","-","+"]
error_message = "X"

class CustomLineEdit(QtWidgets.QLineEdit):
  ''' Class that enables clicking in a text box '''
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
  ''' Class that holds all of the widgets for viewing '''
  def __init__(self):
    ''' Initializes class and variables '''
    super(UIWidget, self).__init__()
    self.prods = 1
    self.prodrulesEdit = []
    self.minuses = None
    self.prodrules = []
    load_saved_lsystems()
    self.initUI()
  def initUI(self):
    ''' Creates and adds all widgets in the viewport and sets the layout  '''
    self.graphix = LSystemDisplayWidget()
    #renames the window
    self.setWindowTitle('L-Systems Generator')

    self.layout = QGridLayout()

    #creates the labels for each text box
    self.axiom = QLabel('Axiom')
    self.prodrules.append(QLabel('Production Rule ' + str(self.prods)))
    self.angle = QLabel('Angles(degrees)')
    self.iters = QLabel('Iterations')

    #creates the text box for each label
    self.axiomEdit = CustomLineEdit()
    self.axiomEdit.clicked.connect(lambda: self.axiomEdit.clear_box())
    self.prodrulesEdit.append(CustomLineEdit())

    self.angleEdit = CustomLineEdit()
    self.angleEdit.clicked.connect(lambda: self.angleEdit.clear_box())
    self.itersEdit = CustomLineEdit()
    self.itersEdit.clicked.connect(lambda: self.itersEdit.clear_box())
    self.prodPlus = QPushButton("+", self)
    self.prodPlus.clicked.connect(self.moreProds)

    self.kochs = QPushButton('Kochs Example')
    self.kochs.clicked.connect(lambda: self.genExample('Koch Snowflake'))

    self.cantor = QPushButton('Cantor Set Example')
    self.cantor.clicked.connect(lambda: self.genExample('Cantor Set'))

    #makes the lsys generator button
    self.lsysbutton = QPushButton("Generate L System", self)
    self.lsysbutton.clicked.connect(self.genLSys)

    self.exitbutton = QPushButton("Exit", self)
    self.exitbutton.clicked.connect(self.cleanup)

    #Adding widgets to window
    self.layout.addWidget(self.axiom, 1, 0)
    self.layout.addWidget(self.axiomEdit, 1, 1, 1, 3)
    self.layout.addWidget(self.prodrules[0], 2, 0)
    self.layout.addWidget(self.prodrulesEdit[0], 2, 1, 1, 1)
    self.layout.addWidget(self.prodPlus, 2, 2, 1, 2)
    self.layout.addWidget(self.angle, 6, 0)
    self.layout.addWidget(self.angleEdit, 6, 1, 1, 3)
    self.layout.addWidget(self.iters, 7, 0)
    self.layout.addWidget(self.itersEdit, 7, 1, 1, 3)
    self.layout.addWidget(self.kochs, 8, 0, 1, 1)
    self.layout.addWidget(self.cantor, 9, 0, 1, 1)
    self.layout.addWidget(self.graphix, 8, 1, 5, -1)
    self.layout.addWidget(self.lsysbutton, 11, 0, 1, 1)
    self.layout.addWidget(self.exitbutton, 12, 0, -1, 1)

    self.setLayout(self.layout)
    self.setGeometry(500, 500, 500, 500)
    self.show()

  def cleanup(self):
      ''' This function cleans the graphics '''
      print("[ INFO ] Exiting...")
      self.graphix.cleanup()

      exit()
  def inputCheck(self):
    '''  This function checks the input
         Returns 1 if valid
         Returns 0 otherwise '''
    valid_input = 1
    axiomInput = self.axiomEdit.text()
    angleInput = self.angleEdit.text()
    itersInput = self.itersEdit.text()
    string = 0
    for ch in axiomInput:
      if not axiomInput in alphabet:
        self.axiomEdit.setStyleSheet("color: red;")
        self.axiomEdit.setText(error_message)
        valid_input = 0
    axiomInProd = 0
    for prod in self.prodrulesEdit:
      prodInput=prod.text()
      prodInput=prodInput.replace(' ','')
      prodInputarr = prodInput.split("->")
      try:
        if prodInputarr[0] == axiomInput:
          axiomInProd = 1
      except:
        axiomInProd =0
    if not axiomInProd:
      self.axiomEdit.setStyleSheet("color: red;")
      self.axiomEdit.setText(error_message)
      valid_input = 0
    #TODO make this work for more than one prod rule
    for prod in self.prodrulesEdit:
      prodInput = prod.text()
      prodInput=prodInput.replace(' ','')
      prodInputarr = prodInput.split("->")

      if not '->' in prodInput or prodInput[1]=='>' or prodInput[len(prodInput)-1]=='>':
        prod.setStyleSheet("color: red;")
        prod.setText(error_message)
        valid_input = 0
      tmp_prodRule = prodInput.replace('->','')

      for ch in tmp_prodRule:
        if not ch in alphabet:
          prod.setStyleSheet("color: red;")
          prod.setText(error_message)
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
      rule = rule.text()
      rule = rule.replace(" ","")
      pr = rule.replace("->",":")
      pr = pr.split(':')
      rules[pr[0]]=pr[1]
    return rules

  def moreProds(self):
    ''' Creates more productions when + button is clicked '''
    if self.prods < len(alphabet):
      self.prods = self.prods + 1
      self.prodrules.append(QLabel("Production Rule " + str(self.prods)))
      self.prodrulesEdit.append(CustomLineEdit())
      self.prodrulesEdit[-1].clicked.connect(lambda: self.prodrulesEdit[-1].clear_box())
      self.layout.addWidget(self.prodrules[self.prods-1], self.prods+1, 0)
      self.layout.addWidget(self.prodrulesEdit[self.prods-1], self.prods+1, 1, 1, 1)

      if self.minuses is not None:
        #remove last minueses
        self.layout.removeWidget(self.minuses)
        self.minuses.deleteLater()
        self.minuses = None

      self.minuses = QPushButton("-", self)
      self.minuses.clicked.connect(self.lessProds)
      self.layout.addWidget(self.minuses, self.prods+1, 2, 1, 2)

  def lessProds(self):
    ''' Removes productions when - button is clicked '''
    if self.prods > 1:
      #remove last widget prodrules
      self.layout.removeWidget(self.prodrules[-1])
      self.prodrules[-1].deleteLater()
      self.prodrules.pop()
      #remove last widget prodrulesEdit
      self.layout.removeWidget(self.prodrulesEdit[-1])
      self.prodrulesEdit[-1].deleteLater()
      self.prodrulesEdit.pop()
      #remove last minueses
      self.layout.removeWidget(self.minuses)
      self.minuses.deleteLater()
      self.minuses = None
      self.prods = self.prods - 1
    if self.prods > 1:
      self.minuses = QPushButton("-", self)
      self.minuses.clicked.connect(self.lessProds)
      self.layout.addWidget(self.minuses, self.prods+1, 2, 1, 2)


  def genLSys(self):
    ''' If the input is valid, iterates through productions and sends to graphics to be drawn '''
    if self.inputCheck():
      axiomInput = self.axiomEdit.text()
      #prodInput = [self.prodrulesEdit.text()] #changed to array
      angleInput = self.angleEdit.text()
      itersInput = self.itersEdit.text()
      print("Axiom: ", axiomInput)
      print("Productions: ")
      #for prod in prodInput:
      #    print(prod)
      print("Angle: ", angleInput)
      print("Iterations: ", itersInput)
      # Format input for use
      rules=self.genRuleDict(self.prodrulesEdit)
      # Generate rule grammar dictionary.
      grammar = {'rules' : rules, 'axiom' : axiomInput, 'iterations' : int(itersInput), 'angle' : float(angleInput)}

      verts = generate_lsystem(grammar)
      # Sets verts on graphics widget and draws
      self.graphix.clear_mesh()
      self.graphix.set_vertices(verts)
      self.graphix.update()

  def genExample(self, example):
    (verts, grammar) = get_saved_lsystem(example)
    self.axiomEdit.setText(grammar['axiom'])
    for key,val in grammar['rules'].items():
      self.prodrulesEdit[0].setText(key+"->"+val)
    #self.prodrulesEdit[0].setText(str(grammar['rules']))
    self.angleEdit.setText(str(grammar["angle"]))
    self.itersEdit.setText(str(grammar['iterations']))
    print(example)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UIWidget()
    sys.exit(app.exec_())
