from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
from lsystem.lsystem_utils import save_lsystem
import sys

class SaveRules(QWidget):
  def __init__(self, ui):
      super().__init__()
      self.ui = ui
      self.init_ui()

  def init_ui(self):
    #sets the window title, layout, and adds widgets to the window
    self.setWindowTitle('Save your rules')
    self.layout = QGridLayout()
    self.create_widgets()
    self.add_widgets()
    self.setLayout(self.layout)

  def create_widgets(self):
    #creates the widgets to be added to the window
    self.save_label = QLabel('Name your rules')
    self.name_box = QLineEdit()
    self.name_box.returnPressed.connect(lambda: self.save())
    self.save_button = QPushButton('Save your rules')
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
      grammar = {}
      grammar["rules"] = {}
      i = 0
      for rule in self.ui.prod_rules_edit:
        print(rule.text())
        rule = rule.text().replace(" ", "")
        pr = rule.split(':')
        #add the rule and probabilty to pr[0]'s list, if there isn't a list then make one
        try:
          grammar["rules"][pr[0]].append([pr[1],self.ui.prod_percent[i].text()])
        except KeyError:
          grammar["rules"][pr[0]] = []
          grammar["rules"][pr[0]].append([pr[1],self.ui.prod_percent[i].text()])
        i += 1 # increment to grab the probability for each rule
      grammar["angle"] = float(self.ui.angle_edit.text())
      if(self.ui.made_angle):
        grammar["turn_angle"] = float(self.ui.turn_angle_edit.text())
      else:
        grammar["turn_angle"] = 0
      if(self.ui.made_line):
        grammar["line_scale"] = float(self.ui.line_scale_edit.text())
      else:
        grammar["line_scale"] = 0
      grammar["axiom"] = self.ui.axiom_edit.text()
      grammar["iterations"] = int(self.ui.iters_edit.text())
      save_lsystem(name, grammar)
      print("[ INFO ] L-System " + str(name) + " saved to disk...")
      #make window disappear
      self.hide()
    else:
      self.name_box.setStyleSheet("color: red;")
      self.name_box.setText("Name your L-System before you save!")
