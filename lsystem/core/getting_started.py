''' Tutorial Page '''

from PyQt5.QtWidgets import (
  QWidget,
  QGridLayout,
  QLabel,
  QPushButton,
  QVBoxLayout,
  QHBoxLayout,
  QStackedWidget,
  QShortcut)
from PyQt5.QtGui import QPixmap

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
    self.pages_widget.setStyleSheet('''
          QLabel#title{
            font-weight: bold;
            font-size: 16px;
            text-decoration: underline;
            text-align: center;}

            QLabel{
                font-size: 14px;
                }
    ''')
    
    self.page_one_widget = QWidget() #axiom
    self.page_one_layout = QGridLayout()
    self.page_two_widget = QWidget() #production rules
    self.page_two_layout = QGridLayout()
    self.page_three_widget = QWidget() #Angle
    self.page_three_layout = QGridLayout()
    self.page_four_widget = QWidget() #iterations
    self.page_four_layout = QGridLayout()
    self.page_five_widget = QWidget() #branching
    self.page_five_layout = QGridLayout()
    self.page_six_widget = QWidget() #turning angle
    self.page_six_layout = QGridLayout()
    self.page_seven_widget = QWidget() #line scale
    self.page_seven_layout = QGridLayout()
    
    self.create_widgets()
    self.add_widgets()
    self.setLayout(self.main_layout)

  def create_widgets(self):
    # creates labels and buttons for the window
    self.axiom_title = QLabel('Axiom', objectName = 'title')
    self.axiom_one = QLabel('The axiom is where your L-System starts.')
    self.axiom_two = QLabel('Use production rules to transform your axiom into an L-System.')
    self.axiom_three = QLabel('See the symbols glossary for valid inputs.')
    self.axiom_screenshot = QLabel(self)
    self.axiom_pic = QPixmap("assets/screenshots/axiom.PNG");
    self.axiom_screenshot.setPixmap(self.axiom_pic)

    self.prod_rule_title = QLabel('Production Rules', objectName = 'title')
    self.prod_rule_one = QLabel('Production rules are part of how you transform your axiom into an L-System.')
    self.prod_rule_two = QLabel('This string will then be used to generate your L-System.')
    self.prod_rule_three = QLabel('Valid rules are in the form X:Y where X is a character or characters in your L-System ' +
                                  'and Y is which character(s) you want to replace it with.')
    self.prod_rule_four = QLabel('The box on the right side is for the weight of the rule.\n' +
                                 'If you only have one rule for a symbol than this box does nothing, ' +
                                 'if you have multiple rules with the same symbol on the left side ' +
                                 'you can weight them so one is chosen more often than the others.')
    self.prod_rule_five = QLabel('The sum of all boxes for a left side must add up to 1.')
    self.prod_rule_six = QLabel('The plus buttons on the right can be used to add up to 3 more production rules to your L-System')
    self.prod_rule_screenshot = QLabel(self)
    self.prod_rule_pic = QPixmap("assets/screenshots/prod_rules.PNG");
    self.prod_rule_screenshot.setPixmap(self.prod_rule_pic)
    
    self.angle_title = QLabel('Angle', objectName = 'title')
    self.angle_one = QLabel('The angle determines how steep the turns are in your L-System when you use + or -.')
    self.angle_two = QLabel('Valid inputs are any number from -360 to 360')
    self.angle_screenshot = QLabel(self)
    self.angle_pic = QPixmap("assets/screenshots/angles.PNG");
    self.angle_screenshot.setPixmap(self.angle_pic)

    self.iteration_title = QLabel('Iterations', objectName = 'title')
    self.iteration_one = QLabel('Iterations affect the number of times rules get applied to the string.')
    self.iteration_two = QLabel('The more iterations, the more defined the shape of your L-System becomes.')
    self.iteration_three = QLabel('Valid inputs are any number greater than 0.')
    self.iteration_screenshot = QLabel(self)
    self.iteration_pic = QPixmap("assets/screenshots/iterations.PNG");
    self.iteration_screenshot.setPixmap(self.iteration_pic)

    self.branching_title = QLabel('Branching', objectName = 'title')
    self.branching_one = QLabel('Branching allows for the L-System to create offshoots')
    self.branching_two = QLabel('You can add a branch by placing symbols between brackets')
    self.branching_three = QLabel('For example [F] will create a straight line branching from the main system')

    self.turn_angle_title = QLabel('Turning Angle', objectName = 'title')
    self.turn_angle_one = QLabel('The turning angle text box only appears if the axiom or a production rule has the symbols ( or ) in it.')
    self.turn_angle_two = QLabel('( decreases the angle by the turning angle and ) increases it.')
    self.turn_angle_three = QLabel('Valid inputs are any number between 0 and 360.')
    self.turn_angle_screenshot = QLabel(self)
    self.turn_angle_pic = QPixmap("assets/screenshots/turn_angle.PNG");
    self.turn_angle_screenshot.setPixmap(self.turn_angle_pic)

    self.line_scale_title = QLabel('Line Scaling', objectName = 'title')
    self.line_scale_one = QLabel('The line scaling text box only appears if the axiom or a production rule has the symbols < or > in it.')
    self.line_scale_two = QLabel('< divides the length of all subsequent lines by the line scaling factor and > increases it.')
    self.line_scale_three = QLabel('Valid inputs are any number')
    self.line_scale_screenshot = QLabel(self)
    self.line_scale_pic = QPixmap("assets/screenshots/line_scale.PNG");
    self.line_scale_screenshot.setPixmap(self.line_scale_pic)
    
    self.next_button = QPushButton("Next Page");
    self.next_button.setShortcut('Ctrl+N')
    self.next_button.clicked.connect(lambda: self.change_page(True))
    self.previous_button = QPushButton("Previous Page");
    self.previous_button.setShortcut('Ctrl+P')
    self.previous_button.clicked.connect(lambda: self.change_page(False))
    
  
  def add_widgets(self):
    # adds widgets to the window
    self.button_layout.addWidget(self.previous_button)
    self.button_layout.addStretch()
    self.button_layout.addWidget(self.next_button)

    self.page_one_layout.addWidget(self.axiom_title, 0, 0)
    self.page_one_layout.addWidget(self.axiom_one, 1, 0)
    self.page_one_layout.addWidget(self.axiom_two, 2, 0)
    self.page_one_layout.addWidget(self.axiom_three, 3, 0)
    self.page_one_layout.addWidget(self.axiom_screenshot,4,0)
    self.page_one_widget.setLayout(self.page_one_layout)
    self.layout_list.append(self.page_one_widget)
    self.pages_widget.addWidget(self.page_one_widget)

    self.page_two_layout.addWidget(self.prod_rule_title, 0, 0)
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

    self.page_three_layout.addWidget(self.angle_title, 0, 0)
    self.page_three_layout.addWidget(self.angle_one, 1, 0)
    self.page_three_layout.addWidget(self.angle_two, 2, 0)
    self.page_three_layout.addWidget(self.angle_screenshot, 3, 0)
    self.page_three_widget.setLayout(self.page_three_layout)
    self.layout_list.append(self.page_three_widget)
    self.pages_widget.addWidget(self.page_three_widget)

    self.page_four_layout.addWidget(self.iteration_title, 0, 0)
    self.page_four_layout.addWidget(self.iteration_one, 1, 0)
    self.page_four_layout.addWidget(self.iteration_two, 2, 0)
    self.page_four_layout.addWidget(self.iteration_three, 3, 0)
    self.page_four_layout.addWidget(self.iteration_screenshot, 4, 0)
    self.page_four_widget.setLayout(self.page_four_layout)
    self.layout_list.append(self.page_four_widget)
    self.pages_widget.addWidget(self.page_four_widget)

    self.page_five_layout.addWidget(self.branching_title, 0, 0)
    self.page_five_layout.addWidget(self.branching_one, 1, 0)
    self.page_five_layout.addWidget(self.branching_two, 2, 0)
    self.page_five_layout.addWidget(self.branching_three, 3, 0)
    self.page_five_widget.setLayout(self.page_five_layout)
    self.layout_list.append(self.page_five_widget)
    self.pages_widget.addWidget(self.page_five_widget)

    self.page_six_layout.addWidget(self.turn_angle_title, 0, 0)
    self.page_six_layout.addWidget(self.turn_angle_one, 1, 0)
    self.page_six_layout.addWidget(self.turn_angle_two, 2, 0)
    self.page_six_layout.addWidget(self.turn_angle_three, 3, 0)
    self.page_six_layout.addWidget(self.turn_angle_screenshot, 4, 0)
    self.page_six_widget.setLayout(self.page_six_layout)
    self.layout_list.append(self.page_six_widget)
    self.pages_widget.addWidget(self.page_six_widget)

    self.page_seven_layout.addWidget(self.line_scale_title, 0, 0)
    self.page_seven_layout.addWidget(self.line_scale_one, 1 ,0)
    self.page_seven_layout.addWidget(self.line_scale_two, 2, 0)
    self.page_seven_layout.addWidget(self.line_scale_three, 3, 0)
    self.page_seven_layout.addWidget(self.line_scale_screenshot, 4, 0)
    self.page_seven_widget.setLayout(self.page_seven_layout)
    self.layout_list.append(self.page_seven_layout)
    self.pages_widget.addWidget(self.page_seven_widget)

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
