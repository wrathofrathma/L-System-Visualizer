from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from lsystem.myUI import *

class myMainWindow(QMainWindow):
  def __init__(self, parent=None):
    super(myMainWindow, self).__init__(parent=parent)
    self.left = 500
    self.top = 500
    self.width = 500
    self.height = 500
    self.initWindow()

  def initWindow(self):
    self.setGeometry(self.left, self.top, self.width, self.height)
    self.initMenus()
    self.show()

  def initMenus(self):
    mainMenu = self.menuBar()
    fileMenu = mainMenu.addMenu('File')
    viewMenu = mainMenu.addMenu('View')
    optionsMenu = mainMenu.addMenu('Options')
    helpMenu = mainMenu.addMenu('Help')


    self.ui_widget = UIWidget()
    self.setCentralWidget(self.ui_widget)

    saveMenu = QMenu('Save', self)
    saveAct = QAction('Take a Screenshot', self)
    saveAct.setShortcut('Ctrl+S')
    saveAct.triggered.connect(lambda: self.saveFile())
    saveMenu.addAction(saveAct)

    exitAction = QAction('Exit', self)
    exitAction.setShortcut('Ctrl+Q')
    exitAction.triggered.connect(lambda: self.closeEvent())

    zoomIn = QAction('Zoom In', self)
    zoomIn.setShortcut('Ctrl++')
    zoomIn.triggered.connect(lambda: self.ui_widget.graphix.zoomIN())

    zoomOut = QAction('Zoom Out', self)
    zoomOut.setShortcut('Ctrl+-')
    zoomOut.triggered.connect(lambda: self.ui_widget.graphix.zoomOUT())

    settings = QAction('Settings', self)
    settings.setShortcut('Ctrl+i')
    settings.triggered.connect(lambda: self.buildPopupSettings())

    fileMenu.addMenu(saveMenu)
    fileMenu.addAction(exitAction)
    viewMenu.addAction(zoomIn)
    viewMenu.addAction(zoomOut)
    optionsMenu.addAction(settings)

  def buildPopupSettings(self):
    self.popupSettings = PopupSettings()
    self.popupSettings.show()

  def saveFile(self):
    options = QFileDialog.Options()
    fileName, _ = QFileDialog.getSaveFileName(self,"Save Screenshot", options=options)
    if fileName:
        self.ui_widget.graphix.screenshot(fileName + ".png")

  def closeEvent(self, event=None):
      print("[ INFO ] Exiting...")
      self.ui_widget.graphix.cleanup()
      exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    display = myMainWindow()
    r = app.exec_()
    sys.exit(r)
