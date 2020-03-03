from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
import sys
from lsystem.myUI import *
from lsystem.glossary import Glossary
from lsystem.getting_started import GettingStarted
from lsystem.screenshot_window import ScreenshotWindow


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent=parent)
        self.left = 500
        self.top = 500
        self.width = 500
        self.height = 500
        self.init_window()

    def init_window(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle('L-System Generator')
        self.init_menus()
        self.show()

    def init_menus(self):
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')
        options_menu = main_menu.addMenu('Options')
        help_menu = main_menu.addMenu('Help')

        self.ui_widget = UIWidget()
        self.setCentralWidget(self.ui_widget)

        save_menu = QMenu('Save', self)
        save_rule_act = QAction('Save L-System Rules', self)
        save_rule_act.triggered.connect(lambda: self.build_save_rules())
        save_menu.addAction(save_rule_act)

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(lambda: self.close_event())

        settings = QAction('Settings', self)
        settings.triggered.connect(lambda: self.build_popup_settings())
        settings.setShortcut('Ctrl+i')

        glossary = QAction('Glossary', self)
        glossary.setShortcut('Ctrl+g')
        glossary.triggered.connect(lambda: self.build_glossary())

        getting_started = QAction('Getting Started', self)
        getting_started.setShortcut('Ctrl+h')
        getting_started.triggered.connect(lambda: self.build_start())

        file_menu.addMenu(save_menu)
        file_menu.addAction(exit_action)
        options_menu.addAction(settings)
        help_menu.addAction(getting_started)
        help_menu.addAction(glossary)

    def build_popup_settings(self):
        self.popup_settings = PopupSettings(self.ui_widget.graphix)
        self.popup_settings.show()

    def build_glossary(self):
        self.glossary = Glossary()
        self.glossary.show()

    def build_start(self):
        self.getting_started = GettingStarted()
        self.getting_started.show()
        
    def build_save_rules(self):
        self.save_rules = SaveRules(self.ui_widget)
        self.save_rules.show()

    def close_event(self, event=None):
        print("[ INFO ] Exiting...")
        self.ui_widget.graphix.cleanup()
        exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    display = MyMainWindow()
    r = app.exec_()
    sys.exit(r)
