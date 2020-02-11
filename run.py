from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from lsystem.myUI import *
from lsystem.glossary import Glossary
from lsystem.getting_started import gettingStarted
from lsystem.save_rules_window import saveRules


class myMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(myMainWindow, self).__init__(parent=parent)
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
        view_menu = main_menu.addMenu('View')
        options_menu = main_menu.addMenu('Options')
        help_menu = main_menu.addMenu('Help')

        self.ui_widget = UIWidget()
        self.setCentralWidget(self.ui_widget)

        save_menu = QMenu('Save', self)
        save_act = QAction('Take a Screenshot', self)
        save_act.setShortcut('Ctrl+S')
        save_act.triggered.connect(lambda: self.save_file())
        save_menu.addAction(save_act)

        save_rule_act = QAction('Save your rules', self)
        save_rule_act.triggered.connect(lambda: self.build_save_rules())
        save_menu.addAction(save_rule_act)

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(lambda: self.close_event())

        zoom_in = QAction('Zoom In', self)
        zoom_in.setShortcut('Ctrl++')
        zoom_in.triggered.connect(lambda: self.ui_widget.graphix.zoom_IN())

        zoom_out = QAction('Zoom Out', self)
        zoom_out.setShortcut('Ctrl+-')
        zoom_out.triggered.connect(lambda: self.ui_widget.graphix.zoom_OUT())

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
        view_menu.addAction(zoom_in)
        view_menu.addAction(zoom_out)
        options_menu.addAction(settings)
        help_menu.addAction(getting_started)
        help_menu.addAction(glossary)

    def build_popup_settings(self):
        self.popup_settings = popup_settings(self.ui_widget.graphix)
        self.popup_settings.show()

    def build_glossary(self):
        self.glossary = Glossary()
        self.glossary.show()

    def build_start(self):
        self.getting_started = getting_started()
        self.getting_started.show()

    def save_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Screenshot", options=options)
        if file_name:
            self.ui_widget.graphix.screenshot(file_name + ".png")

    def build_save_rules(self):
        self.save_rules = save_rules(self.ui_widget)
        self.save_rules.show()

    def close_event(self, event=None):
        print("[ INFO ] Exiting...")
        self.ui_widget.graphix.cleanup()
        exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    display = myMainWindow()
    r = app.exec_()
    sys.exit(r)
