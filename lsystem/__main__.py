"""This file is the run.py that makes the application run"""
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QCheckBox, QToolBar, QLabel, QMainWindow, QApplication, QPushButton, QDialog,
                             QActionGroup,QStatusBar, QMenuBar, QAction, QHBoxLayout, QWidget, QGridLayout)

from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QMenu
from PyQt5.QtCore import QSize, Qt
from lsystem.core.getting_started import GettingStarted
from lsystem.core.glossary import Glossary
from lsystem.core.my_ui import UIWidget
from lsystem.core.save_rules_window import SaveRules
from lsystem.core.settings import PopupSettings

from lsystem.core.lsystem_2d_widget import LSystem2DWidget
from lsystem.core.lsystem_3d_widget import LSystem3DWidget

class MyMainWindow(QMainWindow):
    """This class is the main UI Window that is the parent for the entire application"""

    def __init__(self, parent=None):
        """Defaults the application window to be 500X500"""
        super(MyMainWindow, self).__init__(parent=parent)
        self.left = 500
        self.top = 500
        self.width = 500
        self.height = 500
        self.ui_widget = UIWidget()
        self.popup_settings = PopupSettings(self.ui_widget.graphix)
        self.glossary = Glossary()
        self.save_rules = SaveRules(self.ui_widget)
        self.getting_started = GettingStarted()
        self.init_window()

        toolbar = QToolBar("Settings Toolbar")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)
        toolbar.setMovable(False)
        toolbar.setContextMenuPolicy(Qt.PreventContextMenu)

        self.button_action = QAction("2D", self)
        self.button_action.setStatusTip("Click to use 2D L-Systems!")
        self.button_action.triggered.connect(self.toggle_dim2D)

        self.button_action2 = QAction("3D", self)
        self.button_action2.setStatusTip("Click to use 3D L-Systems!")
        self.button_action2.triggered.connect(self.toggle_dim3D)

        self.save_action = QAction('Save Rules', self)
        self.save_action.setStatusTip("Click to save the grammar of the L-System!")
        self.save_action.triggered.connect(lambda: self.save_rules.show())

        self.glossary_action = QAction("Glossary", self)
        self.glossary_action.setStatusTip("Click to see the glossary!")
        self.glossary_action.triggered.connect(lambda: self.glossary.show())

        self.tutorial = QAction("Tutorial", self)
        self.tutorial.setStatusTip("Click here to see how to get started!")
        self.tutorial.triggered.connect(lambda: self.getting_started.show())

        self.reset_zoom_button = QAction("Reset Zoom",self)
        self.reset_zoom_button.setStatusTip("Click here to reset zoom!")
        self.reset_zoom_button.triggered.connect(self.reset_zoom)

        self.screenshot_button = QAction("Screenshot",self)
        self.screenshot_button.setStatusTip("Click here to take a screenshot!")
        self.screenshot_button.triggered.connect(self.screenshot)

        toolbar.addAction(self.tutorial)
        toolbar.addAction(self.glossary_action)
        toolbar.addAction(self.save_action)
        toolbar.addAction(self.reset_zoom_button)
        toolbar.addAction(self.screenshot_button)

        toolbar.addSeparator()


        toolbar.addAction(self.button_action)
        toolbar.addAction(self.button_action2)

        self.button_action.setCheckable(True)
        self.button_action2.setCheckable(True)
        self.button_action.setChecked(True)

        self.setStatusBar(QStatusBar(self))

        self.setCentralWidget(self.ui_widget)


    def toggle_dim2D(self, s):
        if(s):
          print("I want 2D!")
          self.button_action2.setChecked(False)
          self.ui_widget.dims.setCurrentWidget(self.ui_widget.two_d)
          self.ui_widget.graphix = self.ui_widget.two_d
        else:
          self.button_action.setChecked(True)
          print("Nothing should happen :)")
    def toggle_dim3D(self, s):
        if(s):
            print("I want 3D!")
            self.button_action.setChecked(False)
            self.ui_widget.dims.setCurrentWidget(self.ui_widget.three_d)
            self.ui_widget.graphix = self.ui_widget.three_d
        else:
          self.button_action2.setChecked(True)
          print("Nothing should happen")


    def reset_zoom(self):
        self.ui_widget.reset_zoom()
    def screenshot(self):
        pos = self.pos()
        #pos.setY(self.pos().y()+self.height)
        self.ui_widget.screenshot(pos)

    def init_window(self):
        """Shows the main window"""
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle("L-System Generator")
        self.show()

    def close_event(self):
        """Makes sure everything gets properly deleated upon closing"""
        print("[ INFO ] Exiting...")
        sys.exit()


if __name__ == "__main__":
    APP = QApplication(sys.argv)
    DISPLAY = MyMainWindow()
    R = APP.exec_()
    sys.exit(R)
