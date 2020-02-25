"""This file is the run.py that makes the application run"""
import sys

from PyQt5.QtWidgets import QAction, QApplication, QFileDialog, QMainWindow, QMenu

from lsystem.getting_started import GettingStarted
from lsystem.glossary import Glossary
from lsystem.my_ui import UIWidget
from lsystem.save_rules_window import SaveRules
from lsystem.settings import PopupSettings


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
        view_menu = main_menu.addMenu("View")
        options_menu = main_menu.addMenu("Options")
        help_menu = main_menu.addMenu("Help")

        self.setCentralWidget(self.ui_widget)

        save_menu = QMenu("Save", self)
        save_act = QAction("Take a Screenshot", self)
        save_act.setShortcut("Ctrl+S")
        save_act.triggered.connect(lambda: self.save_file())
        save_menu.addAction(save_act)

        save_rule_act = QAction("Save your rules", self)
        save_rule_act.triggered.connect(lambda: self.save_rules.show())
        save_menu.addAction(save_rule_act)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(lambda: self.close_event())

        zoom_in = QAction("Zoom In", self)
        zoom_in.setShortcut("Ctrl++")
        zoom_in.triggered.connect(lambda: self.ui_widget.graphix.zoom_in())

        zoom_out = QAction("Zoom Out", self)
        zoom_out.setShortcut("Ctrl+-")
        zoom_out.triggered.connect(lambda: self.ui_widget.graphix.zoom_out())

        settings = QAction("Settings", self)
        settings.triggered.connect(lambda: self.popup_settings.show())
        settings.setShortcut("Ctrl+i")

        glossary = QAction("Glossary", self)
        glossary.setShortcut("Ctrl+g")
        glossary.triggered.connect(lambda: self.glossary.show())

        getting_started = QAction("Getting Started", self)
        getting_started.setShortcut("Ctrl+h")
        getting_started.triggered.connect(lambda: self.getting_started.show())

        file_menu.addMenu(save_menu)
        file_menu.addAction(exit_action)
        view_menu.addAction(zoom_in)
        view_menu.addAction(zoom_out)
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
