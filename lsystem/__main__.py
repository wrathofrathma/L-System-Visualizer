"""This file is the run.py that makes the application run"""
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QCheckBox, QToolBar, QLabel, QMainWindow, QApplication, QPushButton, QDialog, 
                             QActionGroup,QStatusBar, QMenuBar, QAction, QHBoxLayout, QWidget, QGridLayout)

from PyQt5.QtWidgets import QAction, QApplication, QFileDialog, QMainWindow, QMenu
from PyQt5.QtCore import QSize, Qt
from lsystem.core.getting_started import GettingStarted
from lsystem.core.glossary import Glossary
from lsystem.core.my_ui import UIWidget
from lsystem.core.save_rules_window import SaveRules
from lsystem.core.settings import PopupSettings

from lsystem.lsystem_2d_widget import LSystem2DWidget
from lsystem.lsystem_3d_widget import LSystem3DWidget

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
        self.button_action.setStatusTip("Click to use 2D L-Systems")
        self.button_action.triggered.connect(self.toggle_dim2D)
        
        self.button_action2 = QAction("3D", self)
        self.button_action2.setStatusTip("Click to use 3D L-Systems")
        self.button_action2.triggered.connect(self.toggle_dim3D)

        toolbar.addAction(self.button_action)
        toolbar.addAction(self.button_action2)
        
        self.button_action.setCheckable(True)
        self.button_action2.setCheckable(True) 
        self.button_action.setChecked(True)
        self.setStatusBar(QStatusBar(self))
    
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
            self.ui_widget.graphc = self.ui_widget.three_d
        else:
          self.button_action2.setChecked(True)
          print("Nothing should happen")
        
         
   
    def init_window(self):
        """Shows the main window"""
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle("L-System Generator")
        self.init_menus()
        self.show()

    def init_menus(self):
        """Makes the menus for the menu bar"""
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("File")
        options_menu = main_menu.addMenu("Options")
        help_menu = main_menu.addMenu("Help")

        self.setCentralWidget(self.ui_widget)

        save_rule_act = QAction("Save your rules", self)
        save_rule_act.triggered.connect(lambda: self.save_rules.show())
        main_menu.addAction(save_rule_act)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(lambda: self.close_event())

        settings = QAction("Settings", self)
        settings.triggered.connect(lambda: self.popup_settings.show())
        settings.setShortcut("Ctrl+i")

        glossary = QAction("Glossary", self)
        glossary.setShortcut("Ctrl+g")
        glossary.triggered.connect(lambda: self.glossary.show())

        getting_started = QAction("Getting Started", self)
        getting_started.setShortcut("Ctrl+h")
        getting_started.triggered.connect(lambda: self.getting_started.show())

        file_menu.addAction(exit_action)
        options_menu.addAction(settings)
        help_menu.addAction(getting_started)
        help_menu.addAction(glossary)

    def save_file(self):
        """Takes a screenshot of the function and saves it"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Screenshot", options=options
        )
        if file_name:
            self.ui_widget.graphix.screenshot(file_name + ".png")

        self.save_rules.show()

    def close_event(self):
        """Makes sure everything gets properly deleated upon closing"""
        print("[ INFO ] Exiting...")
        self.ui_widget.graphix.cleanup()
        sys.exit()


if __name__ == "__main__":
    APP = QApplication(sys.argv)
    DISPLAY = MyMainWindow()
    R = APP.exec_()
    sys.exit(R)
