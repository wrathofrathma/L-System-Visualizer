from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget
from PyQt5.QtGui import QPixmap
import sys

class GettingStarted(QWidget):
  def __init__(self):
      super().__init__()
      self.page_number = 0
      self.layout_list = []
      self.init_ui()

  def init_ui(self):
    #sets window title, layout, and adds the widgets to the window
    self.setWindowTitle('L-System Help')
    self.main_layout = QVBoxLayout()
    self.button_layout = QHBoxLayout()
    self.pages_widget = QStackedWidget()
    
    self.page_one_widget = QWidget()
    self.page_one_layout = QGridLayout()
    self.page_two_widget = QWidget()
    self.page_two_layout = QGridLayout()
    self.page_three_widget = QWidget()
    self.page_three_layout = QGridLayout()
    self.page_four_widget = QWidget()
    self.page_four_layout = QGridLayout()
    
    self.create_widgets()
    self.add_widgets()
    self.setLayout(self.main_layout)

  def create_widgets(self):
    # creates labels and buttons for the window
    self.axiom_one = QLabel('The axiom is where your L-System starts.')
    self.axiom_two = QLabel('Use production rules to transform your axiom into an L-System.')
    self.axiom_three = QLabel('See the symbols glossary for valid inputs.')
    self.axiom_screenshot = QLabel()
    self.axiom_pic = QPixmap('assets/screenshots/axiom.png')
    self.axiom_screenshot.setPixmap(self.axiom_pic)

    self.prod_rule_one = QLabel('Production rules are part of how you transform your axiom into a string.')
    self.prod_rule_two = QLabel('This string will then be used to generate your L-System.')
    self.prod_rule_three = QLabel('Valid rules are in the form X:Y where X is a symbol in the string ' +
                                  'and Y is what symbol(s) you want to replace it with.')
    self.prod_rule_four = QLabel('The small box on the right side is for randomness. ' +
                                 'If you have multiple rules with the same symbol on the left side, ' +
                                 'you can weight them so one is chosen more often than the others.')
    self.prod_rule_five = QLabel('The sum of all boxes for a left side must add up to 1.')
    self.prod_rule_six = QLabel('The plus buttons on the right can be used to add up to 4 production rules to your L-System')
    self.prod_rule_screenshot = QLabel()
    self.prod_rule_pic = QPixmap('assets/screenshots/prod_rules.png')
    self.prod_rule_screenshot.setPixmap(self.prod_rule_pic)

    self.angle_one = QLabel('The angle determines how steep the turns are in your L-System when you use + or -.')
    self.angle_two = QLabel('Valid inputs are any number from 0 to 360')
    self.angle_screenshot = QLabel()
    self.angle_pic = QPixmap('assets/screenshots/angle.png')
    self.angle_screenshot.setPixmap(self.angle_pic)

    self.iteration_one = QLabel('Iterations affect the number of times rules get applied to the string.')
    self.iteration_two = QLabel('The more iterations, the more defined the shape of your L-System becomes.')
    self.iteration_three = QLabel('Valid inputs are any number greater than 0.')
    self.iteration_screenshot = QLabel()
    self.iteration_pic = QPixmap('assets/screenshots/iterations.png')
    self.iteration_screenshot.setPixmap(self.iteration_pic)
    
    self.next_button = QPushButton("Next Page");
    self.next_button.clicked.connect(lambda: self.change_page(True))
    self.previous_button = QPushButton("Previous Page");
    self.previous_button.clicked.connect(lambda: self.change_page(False))
    
  
  def add_widgets(self):
    # adds widgets to the window
    self.button_layout.addWidget(self.previous_button)
    self.button_layout.addStretch()
    self.button_layout.addWidget(self.next_button)
    
    self.page_one_layout.addWidget(self.axiom_one, 1, 0)
    self.page_one_layout.addWidget(self.axiom_two, 2, 0)
    self.page_one_layout.addWidget(self.axiom_three, 3, 0)
    self.page_one_layout.addWidget(self.axiom_screenshot,4,0)
    self.page_one_widget.setLayout(self.page_one_layout)
    self.layout_list.append(self.page_one_widget)
    self.pages_widget.addWidget(self.page_one_widget)

    self.page_two_layout.addWidget(self.prod_rule_one, 1, 0)
    self.page_two_layout.addWidget(self.prod_rule_two, 2, 0)
    self.page_two_layout.addWidget(self.prod_rule_three, 3, 0)
    self.page_two_layout.addWidget(self.prod_rule_four, 4, 0)
    self.page_two_layout.addWidget(self.prod_rule_five, 5, 0)
    self.page_two_layout.addWidget(self.prod_rule_six, 6, 0)
    self.page_two_layout.addWidget(self.prod_rule_screenshot, 7, 0)
    self.page_two_widget.setLayout(self.page_two_layout)
    self.layout_list.append(self.page_two_widget)
    self.pages_widget.addWidget(self.page_two_widget)

    self.page_three_layout.addWidget(self.angle_one, 1, 0)
    self.page_three_layout.addWidget(self.angle_two, 2, 0)
    self.page_three_layout.addWidget(self.angle_screenshot, 3, 0)
    self.page_three_widget.setLayout(self.page_three_layout)
    self.layout_list.append(self.page_three_widget)
    self.pages_widget.addWidget(self.page_three_widget)

    self.page_four_layout.addWidget(self.iteration_one, 1, 0)
    self.page_four_layout.addWidget(self.iteration_two, 2, 0)
    self.page_four_layout.addWidget(self.iteration_three, 3, 0)
    self.page_four_layout.addWidget(self.iteration_screenshot, 4, 0)
    self.page_four_widget.setLayout(self.page_four_layout)
    self.layout_list.append(self.page_four_widget)
    self.pages_widget.addWidget(self.page_four_widget)

    self.main_layout.addWidget(self.pages_widget)
    self.main_layout.addStretch()
    self.main_layout.addLayout(self.button_layout)

  def change_page(self, up):
    if(up):
      self.page_number+=1
      self.page_number%=len(self.layout_list)
    else:
        self.page_number-=1
        if(self.page_number < 0):
          self.page_number+=len(self.layout_list)
          
    self.pages_widget.setCurrentIndex(self.page_number)
