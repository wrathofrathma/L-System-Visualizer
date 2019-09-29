from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QLineEdit, QTextEdit, QGridLayout, QApplication, QLabel
import sys
from PyQt5 import QtWidgets, QtCore
import numpy as np
from math import pi
from lsystem.LSystemWidget import *
from lsystem.Lsystem import *
from lsystem.stack_loop import *


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
    self.prods = 1
    self.prodrulesEdit = []
    self.prodrules = []
    self.initUI()
  def initUI(self):

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
    self.prodrulesEdit.append(CustomLineEdit())
    self.angleEdit = CustomLineEdit()
    self.itersEdit = CustomLineEdit()
    
    self.prodPlus = QPushButton("+", self)
    self.prodPlus.clicked.connect(self.moreProds)
   
    #makes the lsys generator button
    self.lsysbutton = QPushButton("Generate L System", self)
    self.lsysbutton.clicked.connect(self.genLSys)
    
    self.exitbutton = QPushButton("Exit", self)
    self.exitbutton.clicked.connect(exit)
    
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
    self.layout.addWidget(self.graphix, 8, 1, 1, -1)
    self.layout.addWidget(self.lsysbutton, 9, 0)
    self.layout.addWidget(self.exitbutton, 9, 1, -1, -1)
    
    self.setLayout(self.layout)
    self.setGeometry(500, 500, 500, 500)
    self.show()
  
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
    print("prodInput = ", prodInput)
    prodInput=prodInput.replace(' ','')
    print("prodInput = ", prodInput)
    prodInputarr = prodInput.split("->")
    #TODO make this work for more than one prod rule
    if not prodInputarr[0] == axiomInput:
        self.prodrulesEdit.setStyleSheet("color: red;")
        self.prodrulesEdit.setText(error_message)
        valid_input = 0
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
          rule = rule.replace(" ","")
          pr = rule.replace("->",":")
          pr = pr.split(':')
          rules[pr[0]]=pr[1]
      return rules

  def moreProds(self):
    self.prods = self.prods + 1
    if self.prods < 5:
      self.prodrules.append(QLabel("Production Rule " + str(self.prods)))
      self.prodrulesEdit.append(CustomLineEdit())
      self.layout.addWidget(self.prodrules[self.prods-1], self.prods+1, 0)
      self.layout.addWidget(self.prodrulesEdit[self.prods-1], self.prods+1, 1, 1, 1)
      
      self.prodMinus = QPushButton("-", self)
      self.prodMinus.clicked.connect(self.lessProds)
      self.layout.addWidget(self.prodMinus, self.prods+1, 2, 1, 2)


  def lessProds(self):
    #self.prods = self.prods - 1
    #if self.prods > 1:
      #self.layout.removeWidget(self.prodrules[self.prods-1])
      #self.layout.removeWidget(newprodrulesEdit[self.prods-1])
      #self.layout.removeWidget(self.prodMinus)
    print("Maybe someday will delete something")

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
    sys.exit(app.exec_())
