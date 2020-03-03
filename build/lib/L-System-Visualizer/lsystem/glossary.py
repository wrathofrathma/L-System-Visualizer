''' The glossary page '''
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

class Glossary(QWidget):
    ''' Class of the glossary '''
    def __init__(self):
        ''' Initializes the glossary class with all of the labels  '''
        super().__init__()
        self.big_f = QLabel('F: draws a line of unit length.')
        self.little_f = QLabel('f: Moves forward in a line of unit length.')
        self.big_g = QLabel('G: draws a line of unit length.')
        self.little_g = QLabel('g: moves forward in a line of unit length.')
        self.big_h = QLabel('H: draws a line of half unit length.')
        self.little_h = QLabel(
            'h: moves forward in a line of half unit length.')
        self.plus = QLabel('+: turns the angle clockwise by an angle.')
        self.minus = QLabel('-: turns the angle counter-clockwise by an angle.')
        self.pipe = QLabel('|: reverses direction.')
        self.left_bracket = QLabel(
            '[: starts a branch. Must have a ] somewhere after.')
        self.right_bracket = QLabel(
            ']: ends a branch. Must have a [ somewhere before.')
        self.left_parenthesis = QLabel(
            '(: decreases the angle by a turning angle.')
        self.right_parenthesis = QLabel(
            '): increses the angle by a turning angle.')
        self.left_angle = QLabel(
            '<: divides line length by the length factor.')
        self.right_angle = QLabel(
            '>: multiplies the line length by the length factor.')
        self.control = QLabel(
            'A-E, I-Z: Control characters to control how the curve advances')
        self.init_ui()

    def init_ui(self):
        ''' Sets window title, layout, and adds widgets to the window '''
        self.setWindowTitle('Symbol Glossary')
        self.layout = QGridLayout()
        self.add_widgets()
        self.setLayout(self.layout)

    def add_widgets(self):
        ''' Adds the labels to the layout '''
        self.layout.addWidget(self.big_f, 1, 0)
        self.layout.addWidget(self.little_f, 2, 0)
        self.layout.addWidget(self.big_g, 3, 0)
        self.layout.addWidget(self.little_g, 4, 0)
        self.layout.addWidget(self.big_h, 5, 0)
        self.layout.addWidget(self.little_h, 6, 0)
        self.layout.addWidget(self.plus, 7, 0)
        self.layout.addWidget(self.minus, 8, 0)
        self.layout.addWidget(self.left_bracket, 9, 0)
        self.layout.addWidget(self.right_bracket, 10, 0)
        self.layout.addWidget(self.left_parenthesis, 11, 0)
        self.layout.addWidget(self.right_parenthesis, 12, 0)
        self.layout.addWidget(self.left_angle, 13, 0)
        self.layout.addWidget(self.right_angle, 14, 0)
        self.layout.addWidget(self.control, 15, 0)
