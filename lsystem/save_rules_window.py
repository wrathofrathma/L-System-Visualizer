from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
from lsystem.lsystem_utils import save_lsystem
import sys

class saveRules(QWidget):
  def __init__(self, ui):
      super().__init__()
      self.ui = ui
      self.initUI()

  def initUI(self):
    self.setWindowTitle('Save your rules')
    self.layout = QGridLayout()
    self.add_labels()
    self.add_widgets()
    self.setLayout(self.layout)

  def add_labels(self):
    self.saveLabel = QLabel('Name your rules')
    self.nameBox = QLineEdit()
    self.nameBox.returnPressed.connect(lambda: self.save())
    self.saveButton = QPushButton('Save your rules')
    self.saveButton.clicked.connect(lambda: self.save())
  
  def add_widgets(self):
    self.layout.addWidget(self.saveLabel, 1, 0)
    self.layout.addWidget(self.nameBox, 1, 1,1,2)
    self.layout.addWidget(self.saveButton, 1, 3)

  def save(self):
    name = self.nameBox.text()
    if len(name) > 0:
      grammar = {}
      grammar["rules"] = {}
      i = 0
      for rule in self.ui.prodrulesEdit:
        print(rule.text())
        rule = rule.text().replace(" ", "")
        pr = rule.split(':')
        #get probabilities
        try:
          grammar["rules"][pr[0]].append([pr[1],self.ui.prodPercent[i].text()])
        except KeyError:
          grammar["rules"][pr[0]] = []
          grammar["rules"][pr[0]].append([pr[1],self.ui.prodPercent[i].text()])
        i += 1
      grammar["angle"] = float(self.ui.angleEdit.text())
      if(self.ui.madeAngle):
        grammar["turn_angle"] = float(self.ui.turnAngleEdit.text())
      else:
        grammar["turn_angle"] = 0
      if(self.ui.madeLine):
        grammar["line_scale"] = float(self.ui.lineScaleEdit.text())
      else:
        grammar["line_scale"] = 0
      grammar["axiom"] = self.ui.axiomEdit.text()
      grammar["iterations"] = int(self.ui.itersEdit.text())
      save_lsystem(name, grammar)
      print("[ INFO ] L-System " + str(name) + " saved to disk...")
      #make window disappear
      self.hide()
    else:
      self.nameBox.setStyleSheet("color: red;")
      self.nameBox.setText("Name your L-System before you save!")
