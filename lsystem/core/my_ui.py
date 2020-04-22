"""
This file adds the graphics to the UI
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

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QStackedWidget, QVBoxLayout, QPushButton, QWidget, QGridLayout, QLabel, QFileDialog
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from lsystem.core.lsystem_utils import (
    load_saved_lsystems,
    get_saved_lsystem,
    generate_lsystem_2d,
    generate_lsystem_3d,
)
from PyQt5.QtGui import QIcon
from lsystem.core.input_check import input_check

from lsystem.core.lsystem_2d_widget import LSystem2DWidget
from lsystem.core.lsystem_3d_widget import LSystem3DWidget

#from lsystem.core.fractal_dim import fractal_dim_calc
from lsystem.core.fract_menu import FractalDimension, fractal_dim_calc
from lsystem.boxcounting3d.calc import calc_fractal_dim3D
import copy

import os

class CustomLineEdit(QtWidgets.QLineEdit):
    """ Class that enables input in a text box """

    clicked = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.valid = True
        self.error_message = "X"

    # Needs to be CamelCase
    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()

    def reset_color(self):
        self.setStyleSheet("color: black;")

    def clear_box(self):
        self.setText("")
        self.setStyleSheet("color: black;")

    def reset_box(self):
        self.reset_color()
        self.clear_box()



class UIWidget(QWidget):
    """ Class that holds all of the widgets for viewing """

    def __init__(self):
        """ Initializes class and variables """
        super(UIWidget, self).__init__()
        self.axiom = QLabel("Axiom")
        self.angle = QLabel("Angles(degrees)")
        self.iters = QLabel("Iterations")
        self.axiom_edit = CustomLineEdit()
        self.angle_edit = CustomLineEdit()
        self.iters_edit = CustomLineEdit()
        self.text_boxes = [self.axiom_edit, self.angle_edit, self.iters_edit]
        self.prod_plus = QPushButton("+", self)
        self.lsys_button = QPushButton("Generate L System", self)
        self.boxcount_button = QPushButton("Fractal Dim", self)
        
        self.widget = QWidget()
        self.scroll_area = QtWidgets.QScrollArea()
        self.layout_examples = QVBoxLayout(self.widget)

        self.prods = 1
        self.prod_rules_edit = []
        self.examples = []
        self.minuses = None
        self.made_angle = False
        self.prod_percent = []
        self.amount = 0
        self.index = 0
        self.frac_points = []
        self.made_line = False
        self.prod_rules = []
        self.verts = []  # This will store the vertices from generate_lsystem
        self.saved_lsystems = load_saved_lsystems()
        self.two_d = LSystem2DWidget()
        self.three_d = LSystem3DWidget()

        self.fractal_menu = FractalDimension(self)
        self.dims = QStackedWidget()
        self.dims.addWidget(self.two_d)
        self.dims.addWidget(self.three_d)
        self.dims.setCurrentWidget(self.two_d)
        self.graphix = self.two_d

        self.init_UI()
        self.alphabet = [
            "F",
            "f",
            "G",
            "g",
            "H",
            "h",
            "^",
            "&",
            "-",
            "+",
            "[",
            "]",
            "|",
            "(",
            ")",
            ">",
            "<",
            " ",

        ]
        self.ctrl_char = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]

    def init_UI(self):
        """ Creates and adds all widgets in the viewport and sets the layout  """
        # renames the window
        self.setWindowTitle("L-Systems Generator")
        self.layout = QGridLayout()
        self.init_buttons()
        self.init_text_boxes()
        self.add_widgets()
        self.setLayout(self.layout)
        self.setGeometry(500, 500, 500, 500)

    def init_text_boxes(self):
        '''Links all of the text boxes to buttons'''
        # creates the labels for each text box
        self.prod_rules.append(QLabel("Production Rule " + str(self.prods)))

        # creates the text box for each label
        self.axiom_edit.returnPressed.connect(self.lsys_button.click)
        self.axiom_edit.clicked.connect(lambda: self.axiom_edit.reset_color())

        self.prod_rules_edit.append(CustomLineEdit())
        self.prod_rules_edit[0].clicked.connect(
            lambda: self.prod_rules_edit[0].reset_color()
        )
        self.text_boxes.append(self.prod_rules_edit[-1])
        self.prod_rules_edit[0].returnPressed.connect(self.lsys_button.click)
        self.prod_rules_edit[0].textChanged.connect(lambda: self.show_popup())

        self.prod_percent.append(CustomLineEdit())
        self.prod_percent[0].setFixedWidth(50)
        self.prod_percent[0].setText("1")

        self.text_boxes.append(self.prod_percent[-1])
        self.angle_edit.returnPressed.connect(self.lsys_button.click)
        self.angle_edit.clicked.connect(lambda: self.angle_edit.reset_color())

        self.iters_edit.returnPressed.connect(self.lsys_button.click)
        self.iters_edit.clicked.connect(lambda: self.iters_edit.reset_color())

        self.prod_plus.clicked.connect(self.more_prods)

    def init_buttons(self):

        # makes the lsys generator button
        self.lsys_button.clicked.connect(self.on_lsys_button_clicked)
        self.lsys_button.setAutoDefault(True)

        self.boxcount_button.clicked.connect(self.on_boxcount_button_clicked)
        self.boxcount_button.setAutoDefault(True)

        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(150)
        self.scroll_area.setWidget(self.widget)

        precons = ['SierpinksiTriangle', 'KochCurve', 'KochSnowflake',
            'KochIsland', 'PeanoCurve', 'DragonCurve', 'HilbertCurve',
            'TreeExample', 'IslandsandLakes']

        for i, key in enumerate(self.saved_lsystems):
            self.examples.append(QPushButton())
            if i < len(precons):
              self.examples[i].setIcon(QIcon('{}/lsystem/assets/images/{}.png'.format(os.getcwd(), precons[i])))
              self.examples[i].setIconSize(QtCore.QSize(120, 100))
            else:
              self.examples[i].setText(key)
            self.examples[i].clicked.connect(
                lambda state, x=key: self.gen_example(str(x))
            )
            self.layout_examples.addWidget(self.examples[i])
        self.layout_examples.addStretch(1)

    @QtCore.pyqtSlot()
    def on_lsys_button_clicked(self):
        self.gen_sys()

    def boxcount_2d(self):
        """2 dimensional fractal dimension calculation code."""
        self.fractal_menu.show()
        start_size = 8
        num_sizes = 7
        self.x_arr = []
        self.y_arr = []
        fract_avg = []
        end_size = start_size * (2 ** num_sizes)
        temp_verts = copy.deepcopy(self.verts)
        fractal_dim = fractal_dim_calc(temp_verts, end_size, num_sizes)
        for i in range(num_sizes):
            self.x_arr.append(np.log2((start_size)))
            self.y_arr.append(fractal_dim[i])

            fract_avg.append(np.polyfit(self.x_arr, self.y_arr, 1)[0])
            print("(box width = 1/", start_size, ") FRACTAL AVG: ", fract_avg[-1])
            start_size = start_size * 2
        # y_arr = np.asarray(y_arr)
        # x_arr = np.asarray(x_arr)
        print("Made it this far")
        figi, ax = plt.subplots()
        line, = ax.plot(self.x_arr, self.y_arr, "bo", picker=5)
        ax.set_title(
            "Fractal dimension = {}".format(np.polyfit(self.x_arr, self.y_arr, 1)[0])
        )  # np.average(fract_avg)))
        figi.canvas.mpl_connect('pick_event', self.onpick1)
        #figi.show()
        plt.show()
        print("AVERAGE: ", np.average(fract_avg))

    def boxcount_3d(self):
        """3 dimensional fractal dimension calc code. I'll have to do some data sanitization somewhere. Maybe here."""
        mesh = self.graphix.mesh
        if(mesh is not None):
            calc_fractal_dim3D(mesh)


    def is_2d(self):
        """Returns true if 2D is loaded, false if 3D is loaded."""
        if (self.dims.currentWidget().__class__.__name__ == 'LSystem3DWidget'):
            return False
        return True

    def on_boxcount_button_clicked(self):
        if(self.is_2d()):
            self.boxcount_2d()
        else:
            self.boxcount_3d()

    def onpick1(self, event):
        print("I am an EVENT1")
        #plt.close(fig=None)
        ind = event.ind[0]+1
        for i in range(ind):
            if(len(self.x_arr)==2):
                break
            # always delete index 0 because array shifts left after delete
            self.x_arr = np.delete(self.x_arr, 0, axis=None)
            self.y_arr = np.delete(self.y_arr, 0, axis=None)
        print("The x array is: ", self.x_arr)
        fig1, ax = plt.subplots()
        ax.plot(self.x_arr, self.y_arr, "bo", picker=5)
        ax.set_title(
            "Fractal dimension = {}".format(np.polyfit(self.x_arr, self.y_arr, 1)[0])
        )  # np.average(fract_avg)))
        fig1.canvas.mpl_connect('pick_event', self.onpick2)
        fig1.show()
        return True
    def onpick2(self, event):
        print("I am an EVENT2")
        #plt.close(fig=None)
        ind = event.ind[0]
        num_to_remove = len(self.x_arr)-ind
        for i in range(num_to_remove):
            if(len(self.x_arr)==2):
                break
            # always delete index -1
            self.x_arr = np.delete(self.x_arr, -1, axis=None)
            self.y_arr = np.delete(self.y_arr, -1, axis=None)
        fig2, ax = plt.subplots()
        ax.plot(self.x_arr, self.y_arr, "bo", picker=5)
        ax.set_title(
            "Fractal dimension = {}".format(np.polyfit(self.x_arr, self.y_arr, 1)[0])
        )  # np.average(fract_avg)))
        fig2.show()
        return True



    def add_widgets(self):
        # Adding widgets to window
        self.layout.addWidget(self.axiom, 1, 0)
        self.layout.addWidget(self.axiom_edit, 1, 1, 1, 10)
        self.layout.addWidget(self.prod_rules[0], 2, 0, 1, 1)
        self.layout.addWidget(self.prod_rules_edit[0], 2, 1, 1, 9)
        self.layout.addWidget(self.prod_percent[0], 2, 9)
        self.layout.addWidget(self.prod_plus, 2, 10, 1, 1)
        self.layout.addWidget(self.angle, 10, 0)
        self.layout.addWidget(self.angle_edit, 10, 1, 1, 10)
        self.layout.addWidget(self.iters, 13, 0)
        self.layout.addWidget(self.iters_edit, 13, 1, 1, 10)
        self.layout.addWidget(self.scroll_area, 14, 0, 1, 1)
        self.layout.addWidget(self.boxcount_button, 16, 0, 1, 1)
        self.layout.addWidget(self.dims, 14, 1, 5, -1)
        self.layout.addWidget(self.lsys_button, 20, 0, 1, -1)

    def show_popup(self):
        self.reset_text_box_color()
        prod_rule = ""
        rules = ""
        self.amount = 0
        for prod in self.prod_rules_edit:
            prod_rule += prod.text()
            temp = prod.text()
            temp = temp.replace(" ", "")
            temp = temp[:].split(":")[0]
            rules += temp
            rules += " "

        all_prod_rule = prod_rule + self.axiom_edit.text()

        if (")" in all_prod_rule or "(" in all_prod_rule) and self.made_angle is False:
            self.turn_angle = QLabel("Turning Angle")
            self.turn_angle_edit = CustomLineEdit()
            self.text_boxes.append(self.turn_angle_edit)
            self.turn_angle_edit.returnPressed.connect(self.lsys_button.click)
            self.turn_angle_edit.clicked.connect(
                lambda: self.turn_angle_edit.reset_color()
            )
            self.layout.addWidget(self.turn_angle, 11, 0)
            self.layout.addWidget(self.turn_angle_edit, 11, 1, 1, 10)
            self.made_angle = True

        if (
            self.made_angle is True
            and not "(" in all_prod_rule
            and not ")" in all_prod_rule
            and self.made_angle is True
        ):
            self.text_boxes.remove(self.turn_angle_edit)
            self.layout.removeWidget(self.turn_angle_edit)
            self.layout.removeWidget(self.turn_angle)
            self.turn_angle.deleteLater()
            self.turn_angle_edit.deleteLater()
            self.turn_angle_edit = None
            self.turn_angle = None
            self.made_angle = False

        if (">" in all_prod_rule or "<" in all_prod_rule) and self.made_line is False:
            self.line_scale = QLabel("Line Scale")
            self.line_scale_edit = CustomLineEdit()
            self.text_boxes.append(self.line_scale_edit)
            self.line_scale_edit.returnPressed.connect(self.lsys_button.click)
            self.line_scale_edit.clicked.connect(
                lambda: self.line_scale_edit.reset_color()
            )
            self.layout.addWidget(self.line_scale, 12, 0)
            self.layout.addWidget(self.line_scale_edit, 12, 1, 1, 10)
            self.made_line = True

        if (
            self.made_line is True
            and not "<" in all_prod_rule
            and not ">" in all_prod_rule
            and self.made_line is True
        ):
            self.text_boxes.remove(self.line_scale_edit)
            self.layout.removeWidget(self.line_scale_edit)
            self.layout.removeWidget(self.line_scale)
            self.line_scale.deleteLater()
            self.line_scale_edit.deleteLater()
            self.line_scale_edit = None
            self.line_scale = None
            self.made_line = False

    # Probably doesn't need self as a param, can just be static.
    # Generates a rule dictionary from an array of production rule strings taken from the UI
    def gen_rule_dict(self, prod_rules):
        """
        formats production rules as
        {"F": [[p,rule],[p,rule]], "f":[[p,rule],[p,rule]] ... }
        """
        rules = {}
        for rule in prod_rules:
            rule = rule.text()
            rule = rule.replace(" ", "")
            prod = rule.split(":")
            rules[prod[0]] = []
        for i, rule in enumerate(prod_rules):
            rule = rule.text()
            rule = rule.replace(" ", "")
            prod = rule.split(":")
            rules[prod[0]].append([float(self.prod_percent[i].text()), prod[1]])
        return rules

    def close_event(self):
        print("[ INFO ] Exiting...")
        exit()

    def more_prods(self):
        """ Creates more productions when + button is clicked """
        if self.prods < 4:
            self.prods = self.prods + 1
            self.prod_rules.append(QLabel("Production Rule " + str(self.prods)))
            self.prod_rules_edit.append(CustomLineEdit())
            self.prod_percent.append(CustomLineEdit())
            self.text_boxes.append(self.prod_rules_edit[-1])
            self.text_boxes.append(self.prod_percent[-1])
            self.prod_percent[-1].setFixedWidth(50)
            self.prod_rules_edit[self.prods - 1].textChanged.connect(
                lambda: self.show_popup()
            )
            self.prod_rules_edit[-1].returnPressed.connect(self.lsys_button.click)
            self.prod_rules_edit[-1].clicked.connect(
                lambda: self.prod_rules_edit[-1].reset_color()
            )
            self.layout.addWidget(self.prod_rules[self.prods - 1], self.prods + 1, 0)
            self.layout.addWidget(
                self.prod_rules_edit[self.prods - 1], self.prods + 1, 1, 1, 9
            )
            self.layout.addWidget(self.prod_percent[self.prods - 1], self.prods + 1, 9)

            if self.minuses is not None:
                # remove last minueses
                self.layout.removeWidget(self.minuses)
                self.minuses.deleteLater()
                self.minuses = None

            self.minuses = QPushButton("-", self)
            self.minuses.clicked.connect(self.less_prods)
            self.layout.addWidget(self.minuses, self.prods + 1, 10, 1, 1)
            self.prod_percent[-1].setText("1")

    def less_prods(self):
        """ Removes productions when - button is clicked """
        if self.prods > 1:
            self.text_boxes.remove(self.prod_rules_edit[-1])
            self.text_boxes.remove(self.prod_percent[-1])

            # remove last widget prodrules
            self.layout.removeWidget(self.prod_rules[-1])
            self.prod_rules[-1].deleteLater()
            self.prod_rules.pop()
            # remove last widget prodrulesEdit
            self.layout.removeWidget(self.prod_rules_edit[-1])
            self.prod_rules_edit[-1].deleteLater()
            self.prod_rules_edit.pop()
            # remove last percentage
            self.layout.removeWidget(self.prod_percent[-1])
            self.prod_percent[-1].deleteLater()
            self.prod_percent.pop()
            # remove last percentage
            # for i in self.index:
            #    for j in i:
            #        if j == self.prods-1:
            #             print("WE NEED TO DELETE")
            #             print(i)
            #      print("HELLO")
            #      self.layout.removeWidget(self.prodPercent[-1])
            #      self.prodPercent[-1].deleteLater()
            #      self.prodPercent.pop()
            #      self.amount = self.amount - 1
            #      print(len(self.prodPercent))
            # remove last minuses
            self.layout.removeWidget(self.minuses)
            self.minuses.deleteLater()
            self.minuses = None
            self.prods = self.prods - 1


        if self.prods > 1:
            self.minuses = QPushButton("-", self)
            self.minuses.clicked.connect(self.less_prods)
            self.layout.addWidget(self.minuses, self.prods + 1, 10, 1, 1)

    def gen_sys(self):

        """
        If the input is valid, iterates through productions
        and sends to graphics to be drawn
        """
        if input_check(self):
            axiom_input = self.axiom_edit.text()
            # prodInput = [self.prodrlesEdit.text()] #changed to array
            angle_input = self.angle_edit.text()
            if self.made_angle:
                turn_angle_input = self.turn_angle_edit.text()
            else:
                turn_angle_input = 0
            if self.made_line:
                line_scale_input = self.line_scale_edit.text()
            else:
                line_scale_input = 1
            iters_input = self.iters_edit.text()
            # Format input for use
            rules = self.gen_rule_dict(self.prod_rules_edit)
            # Generate rule grammar dictionary.
            grammar = {
                "rules": rules,
                "axiom": axiom_input,
                "iterations": int(iters_input),
                "angle": float(angle_input),
                "turnAngle": float(turn_angle_input),
                "lineScale": float(line_scale_input),
            }
            if (self.dims.currentWidget().__class__.__name__ == 'LSystem3DWidget'):
              self.mesh = generate_lsystem_3d(grammar)
              self.graphix.clear()
              self.graphix.add_mesh(self.mesh)
            else:
              self.verts = generate_lsystem_2d(grammar)
              # Sets verts on graphics widget and draws
              self.graphix.clear()
              self.graphix.set_graph(self.verts)
            # for i in range(1,len(self.verts)):
            #  self.graphix.set_graph(self.verts[i],1) #split = true
        self.graphix.update()
        self.graphix.reset_camera()

    def gen_example(self, example):
        self.axiom_edit.reset_box()
        for prod in self.prod_rules_edit:
            prod.reset_box()
        self.angle_edit.reset_box()
        self.iters_edit.reset_box()
        grammar = get_saved_lsystem(example, self.saved_lsystems)
        self.axiom_edit.setText(grammar["axiom"])

        num_rules = 0
        for key in grammar["rules"]:
            if isinstance(grammar["rules"][key], list):
                num_rules += len(grammar["rules"][key])
            else:
                num_rules += 1

        while self.prods < num_rules:
            self.more_prods()

        while self.prods > num_rules:
            self.less_prods()

        which_rule = 0
        for i, key in enumerate(grammar["rules"]):
            value = grammar["rules"][key]
            if isinstance(value, str):
                self.prod_rules_edit[which_rule].setText(key + ": " + value)
                which_rule+=1
            else:
                for val in value:
                    print(val)
                    self.prod_rules_edit[which_rule].setText(key + ": " + val[0])
                    self.prod_percent[which_rule].setText(val[1])
                    which_rule+=1

        self.angle_edit.setText(str(grammar["angle"]))
        if self.made_angle:
            self.turn_angle_edit.setText(str(grammar["turn_angle"]))
        if self.made_line:
            self.line_scale_edit.setText(str(grammar["line_scale"]))
        self.iters_edit.setText(str(grammar["iterations"]))
        self.gen_sys()

    def reset_text_box_color(self):
        for box in self.text_boxes:
            box.reset_color()
    def reset_zoom(self):
        self.two_d.reset_zoom()
        self.three_d.reset_zoom() #built in function don't change to snake script
    def screenshot(self, parent_pos):
        #rel pos is the upper left pointof the widget relative to window
        rel_pos = self.dims.pos()
        #shift the y down by the total height - height of the widget (height of text boxes)
        #1.1 factor added arbitrarily
        rel_pos.setY((self.height()-self.dims.height())*1.1)
        pos =  rel_pos+parent_pos
        qfd = QFileDialog()
        filter = "Images (*.png *.xpm *.jpg)"
        filename, type = QFileDialog.getSaveFileName(self, "", "", filter)
        if filename:
            self.two_d.screenshot(filename,pos)

