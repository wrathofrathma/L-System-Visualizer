''' The glossary page '''
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

class Glossary(QWidget):
    ''' Class of the glossary '''
    def __init__(self, dim):
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
        self.plus_3D = QLabel('+: turns counter-clockwise on the xy-plane')
        self.minus_3D = QLabel('-: turns clockwise on the xy-plane')
        self.left_angle_3D = QLabel('<: turns counter-clockwise on the xz-plane')
        self.right_angle_3D = QLabel('>: turns clockwise on the xz-plane')
        self.carat_3D = QLabel('^: turns counter-clockwise on the yz-plane')
        self.ampersand_3D = QLabel('&: turns clockwise on the yz-plane')
        self.dim = dim
        self.init_ui()

    def init_ui(self):
        ''' Sets window title, layout, and adds widgets to the window '''
        self.setWindowTitle('Symbol Glossary')
        self.layout = QGridLayout() 
        self.setStyleSheet('''
              QLabel#title{
                font-weight: bold;
                font-size: 16px;
                text-decoration: underline;
                text-align: center;}

                QLabel{
                    font-size: 14px;
                    }
        ''')
        self.add_widgets()
        self.setLayout(self.layout)

    def add_widgets(self):
        ''' Adds the labels to the layout '''
        self.layout.addWidget(self.big_f, 1, 0)
        self.layout.addWidget(self.little_f, 2, 0)
        self.layout.addWidget(self.big_g, 3, 0)
        self.layout.addWidget(self.little_g, 4, 0)
        self.layout.addWidget(self.left_bracket, 5, 0)
        self.layout.addWidget(self.right_bracket, 6, 0)
        if self.dim == 2:
            self.layout.addWidget(QLabel("2D Symbols", objectName = 'title'), 0, 0);
            self.layout.addWidget(self.big_h, 7, 0)
            self.layout.addWidget(self.little_h, 8, 0)
            self.layout.addWidget(self.plus, 9, 0)
            self.layout.addWidget(self.minus, 10, 0)
            self.layout.addWidget(self.pipe, 11, 0)
            self.layout.addWidget(self.left_parenthesis, 12, 0)
            self.layout.addWidget(self.right_parenthesis, 13, 0)
            self.layout.addWidget(self.left_angle, 14, 0)
            self.layout.addWidget(self.right_angle, 15, 0)
        else:
            self.layout.addWidget(QLabel("3D Symbols", objectName = 'title'), 0, 0);
            self.layout.addWidget(self.plus_3D, 7, 0)
            self.layout.addWidget(self.minus_3D, 8, 0)
            self.layout.addWidget(self.left_angle_3D, 9, 0)
            self.layout.addWidget(self.right_angle_3D, 10, 0)
            self.layout.addWidget(self.carat_3D, 11, 0)
            self.layout.addWidget(self.ampersand_3D, 12, 0)
        self.layout.addWidget(self.control, 16, 0)
