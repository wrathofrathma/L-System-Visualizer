from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QLineEdit, QTextEdit, QGridLayout, QApplication, QLabel
import sys
from PyQt5 import QtWidgets, QtCore
import numpy as np
from math import pi
from lsystem.LSystemWidget import *
from lsystem.lsystem_utils import *

"""
F(and G) draws a unit length line
f(and g) moves forward a unit length
H draws a half length line
h moves forward half a unit length
- turns counter-clockwise
+ turns clockwise
[ starts branch
] ends branch
| reverses direction
( decrements the angle by a turning angle
) increments the angle by a turning angle
"""
alphabet = ["F","f","G","g","H","h","-","+","[","]","|", "(", ")", ">", "<"]
ctrl_char = ['A','B','C','D','E','I','J','K','L,','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
error_message = "X"

class customLineEdit(QtWidgets.QLineEdit):
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
    self.examples = []
    self.minuses = None
    self.prodrules = []
    load_saved_lsystems()
    self.graphix = LSystemDisplayWidget()
    self.initUI()

  def initUI(self):
    ''' Creates and adds all widgets in the viewport and sets the layout  '''
    #renames the window
    self.setWindowTitle('L-Systems Generator')
    self.layout = QGridLayout()
    self.initButtons()
    self.initTextBoxes()
    self.addWidgets()
    self.setLayout(self.layout)
    self.setGeometry(500, 500, 500, 500)

  def initTextBoxes(self):
    #creates the labels for each text box
    self.axiom = QLabel('Axiom')
    self.prodrules.append(QLabel('Production Rule ' + str(self.prods)))
    self.angle = QLabel('Angles(degrees)')
    self.iters = QLabel('Iterations')
    self.turnAngle = QLabel('Turning Angle')
    self.lineScale = QLabel('Line Scale')

    #creates the text box for each label
    self.axiomEdit = customLineEdit()
    self.axiomEdit.returnPressed.connect(self.lsysbutton.click)
    self.axiomEdit.clicked.connect(lambda: self.axiomEdit.clear_box())
    
    self.prodrulesEdit.append(customLineEdit())
    self.prodrulesEdit[-1].clicked.connect(lambda: self.prodrulesEdit[-1].clear_box()) 
    self.prodrulesEdit[-1].returnPressed.connect(self.lsysbutton.click)

    self.angleEdit = customLineEdit()
    self.angleEdit.returnPressed.connect(self.lsysbutton.click)
    self.angleEdit.clicked.connect(lambda: self.angleEdit.clear_box())

    self.itersEdit = customLineEdit()
    self.itersEdit.returnPressed.connect(self.lsysbutton.click)
    self.itersEdit.clicked.connect(lambda: self.itersEdit.clear_box())

    self.prodPlus = QPushButton("+", self)
    self.prodPlus.clicked.connect(self.moreProds)

    self.turnAngleEdit = customLineEdit()
    self.turnAngleEdit.returnPressed.connect(self.lsysbutton.click)
    self.turnAngleEdit.clicked.connect(lambda: self.turnAngleEdit.clear_box())

    self.lineScaleEdit = customLineEdit()
    self.lineScaleEdit.returnPressed.connect(self.lsysbutton.click)
    self.lineScaleEdit.clicked.connect(lambda: self.lineScaleEdit.clear_box())


  def initButtons(self):

    #makes the lsys generator button
    self.lsysbutton = QPushButton("Generate L System", self)
    self.lsysbutton.clicked.connect(self.on_lsysbutton_clicked)
    self.lsysbutton.setAutoDefault(True)

    self.widget = QWidget()
    self.scrollArea = QtWidgets.QScrollArea()
    self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.scrollArea.setWidgetResizable(True)
    self.scrollArea.setFixedWidth(150)
    self.scrollArea.setWidget(self.widget)
    self.layout_examples = QVBoxLayout(self.widget)

    for i, key in enumerate(saved_lsystems):
     self.examples.append(QPushButton(key))
     self.examples[i].clicked.connect(lambda state, x=key: self.genExample(str(x)))
     self.layout_examples.addWidget(self.examples[i])
    self.layout_examples.addStretch(1)
  
  @QtCore.pyqtSlot()
  def on_lsysbutton_clicked(self):
    self.genLSys()
  
  def addWidgets(self):

    #Adding widgets to window
    self.layout.addWidget(self.axiom, 1, 0)
    self.layout.addWidget(self.axiomEdit, 1, 1, 1, 3)
    self.layout.addWidget(self.prodrules[0], 2, 0)
    self.layout.addWidget(self.prodrulesEdit[0], 2, 1, 1, 1)
    self.layout.addWidget(self.prodPlus, 2, 2, 1, 2)
    self.layout.addWidget(self.angle, 10, 0)
    self.layout.addWidget(self.angleEdit, 10, 1, 1, 3)
    self.layout.addWidget(self.turnAngle, 11, 0)
    self.layout.addWidget(self.turnAngleEdit, 11, 1, 1, 3)
    self.layout.addWidget(self.lineScale, 12, 0)
    self.layout.addWidget(self.lineScaleEdit, 12, 1, 1, 3)
    self.layout.addWidget(self.iters, 13, 0)
    self.layout.addWidget(self.itersEdit, 13, 1, 1, 3)
    self.layout.addWidget(self.scrollArea, 14, 0, 1, 1)
    self.layout.addWidget(self.graphix, 14, 1, 5, -1)
    self.layout.addWidget(self.lsysbutton, 20, 0, 1, -1)


  def inputCheck(self):
    '''  This function checks the input
         Returns 1 if valid
         Returns 0 otherwise '''
    ctrl_char_lhs=[] #control chars that are on the left hand side of a rule
    valid_input = 1
    axiomInput = self.axiomEdit.text()
    angleInput = self.angleEdit.text()
    turnAngleInput = self.turnAngleEdit.text()
    lineScaleInput = self.lineScaleEdit.text()
    itersInput = self.itersEdit.text()
    string = 0
    if len(axiomInput)==0:
      self.axiomEdit.setStyleSheet("color: red;")
      self.axiomEdit.setText(error_message)
      valid_input = 0
    for ch in axiomInput:
      if not (ch in alphabet or ch in ctrl_char):
        print("[ ERROR ] ",ch," not in alphabet")
        self.axiomEdit.setStyleSheet("color: red;")
        self.axiomEdit.setText(error_message)
        valid_input = 0
    axiomInProd = 0

    for prod in self.prodrulesEdit:
      prodInput = prod.text()
      prodInput=prodInput.replace(' ','')
      prodInputarr = prodInput.split("->")

      if not '->' in prodInput:
        prod.setStyleSheet("color: red;")
        prod.setText(error_message)
        valid_input = 0
      tmp_prodRule = prodInput.replace('->','')
      stack = []
      prevCh=''
      for ch in tmp_prodRule:
        if ch == '[':
          stack.append(ch)
        if ch == ']':
          if prevCh =='[':
              print("[ ERROR ] Branches should be non-empty")
              prod.setStyleSheet("color: red;")
              prod.setText(error_message)
              valid_input = 0
          if len(stack)==0:
            print("[ ERROR ] Each production rule must have balanced brackets")
            prod.setStyleSheet("color: red;")
            prod.setText(error_message)
            valid_input = 0
          else:
            stack.pop()
        if not (ch in alphabet or ch in ctrl_char):
          prod.setStyleSheet("color: red;")
          prod.setText(error_message)
          valid_input = 0
        prevCh=ch
      if len(stack)!=0:
        print("[ ERROR ] Each production rule must have balanced brackets")
        prod.setStyleSheet("color: red;")
        prod.setText(error_message)
        valid_input = 0
      tmp_prodRule = prodInput.split('->')
      for ch in tmp_prodRule[0]:
        if ch in ctrl_char:
          ctrl_char_lhs.append(ch)
    for prod in self.prodrulesEdit:
      tmp_prodRule = prodInput.split('->')
      for ch in tmp_prodRule[1]:
        if ch in ctrl_char and not ch in ctrl_char_lhs:
          print("[ ERROR ] Control characters must be the key to a rule")
          prod.setStyleSheet("color: red;")
          prod.setText(error_message)
          valid_input = 0
    for ch in axiomInput:
      if ch in ctrl_char and not ch in ctrl_char_lhs:
        print("[ ERROR ] Control characters must be the key to a rule")
        self.axiomEdit.setStyleSheet("color: red;")
        self.axiomEdit.setText(error_message)
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
      turnAngleInput = float(turnAngleInput)
    except:
      self.turnAngleEdit.setStyleSheet("color: red;")
      self.turnAngleEdit.setText("X")
      valid_input=0
      string = 1 #is a string
    if not string:
      if turnAngleInput <= -360 or turnAngleInput >= 360:
        self.turnAngleEdit.setStyleSheet("color: red;")
        self.turnAngleEdit.setText(error_message)
        valid_input = 0

    try:
      lineScaleInput = float(lineScaleInput)
    except:
      self.lineScaleEdit.setStyleSheet("color: red;")
      self.lineScaleEdit.setText(error_message)
      valid_input = 0
      string = 1 #is a string
    if not string:
      if lineScaleInput <= 0:
        self.lineScaleEdit.setStyleSheet("color: red;")
        self.lineScaleEdit.setText(error_message)
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
    non_det = 1
    if non_det == 0:
      rules = {}
      for rule in prodRules:
        rule = rule.text()
        rule = rule.replace(" ","")
        pr = rule.replace("->",":")
        pr = pr.split(':')
        rules[pr[0]] = pr[1]
      '''
      THIS PART IS NOT CONTEXT SENSITIVE
      '''
      for letter in alphabet:
        if not letter in list(rules.keys()):
          rules[letter] = letter
      return rules
    elif non_det == 1:
      #formats production rules as
      """
      {"F": [[p,rule],[p,rule]], "f":[[p,rule],[p,rule]] ... }
      """
      rules = {}
      #for r in alphabet:
      #  rules[r]=[]
      for rule in prodRules:
        rule = rule.text()
        rule = rule.replace(" ","")
        pr = rule.replace("->",":")
        pr = pr.split(':')
        rules[pr[0]]=[]
      for rule in prodRules:
        rule = rule.text()
        rule = rule.replace(" ","")
        pr = rule.replace("->",":")
        pr = pr.split(':')
        rules[pr[0]].append([0,pr[1]])
      '''
      THIS PART IS NOT CONTEXT SENSITIVE
      '''

      for key in rules.keys():
        #r is random array of prob that add to 1
        l=len(rules[key])
        r = [rand.random() for i in range(1,l+1)]
        s = sum(r)
        r = [ i/s for i in r ]
        for i in range(l):
          rules[key][i][0] = r[i]
      #for letter in alphabet:
      #  if len(rules[letter])==0:
      #    rules[letter].append([1,letter])
      return rules

  def closeEvent(self, event):
      print("[ INFO ] Exiting...")
      self.graphix.cleanup()
      exit()

  def moreProds(self):
    ''' Creates more productions when + button is clicked '''
    if self.prods < 4:
      self.prods = self.prods + 1
      self.prodrules.append(QLabel("Production Rule " + str(self.prods)))
      self.prodrulesEdit.append(customLineEdit())
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
      turnAngleInput = self.turnAngleEdit.text()
      lineScaleInput = self.lineScaleEdit.text()
      itersInput = self.itersEdit.text()
      print("Axiom: ", axiomInput)
      print("Productions: ")
      #for prod in prodInput:
      #    print(prod)
      print("Angle: ", angleInput)
      print("Turning Angle: ", turnAngleInput)
      print("Line Scale: ", lineScaleInput)
      print("Iterations: ", itersInput)
      # Format input for use
      rules=self.genRuleDict(self.prodrulesEdit)
      # Generate rule grammar dictionary.
      grammar = {'rules' : rules, 'axiom' : axiomInput, 'iterations' : int(itersInput), 'angle' : float(angleInput), 'turnAngle': float(turnAngleInput), 'lineScale': float(lineScaleInput)}
      verts = generate_lsystem(grammar)
      # Sets verts on graphics widget and draws
      self.graphix.clear_mesh()
      self.graphix.set_vertices(verts[0])
      for i in range(1,len(verts)):
        self.graphix.set_vertices(verts[i],1) #split = true
      self.graphix.update()
      self.graphix.resetCamera()

  def genExample(self, example):
    self.axiomEdit.clear_box()
    for p in self.prodrulesEdit:
      p.clear_box()
    self.angleEdit.clear_box()
    self.itersEdit.clear_box()
    #(verts, grammar) = get_saved_lsystem(example)
    grammar = get_saved_lsystem(example)
    self.axiomEdit.setText(grammar['axiom'])
    while self.prods < len(grammar['rules']):
      self.moreProds()

    while self.prods > len(grammar['rules']):
      self.lessProds()

    for i, key in enumerate(grammar['rules']):
      value = grammar['rules'][key]
      self.prodrulesEdit[i].setText(key+"->"+value)
    self.angleEdit.setText(str(grammar["angle"]))
    self.turnAngleEdit.setText(str(grammar['turn_angle']))
    self.lineScaleEdit.setText(str(grammar['line_scale']))
    self.itersEdit.setText(str(grammar['iterations']))
    self.genLSys()
    #print(example)

