from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QLineEdit, QTextEdit, QGridLayout, QApplication, QLabel
import sys

class UIWidget(QWidget): 
  
  def __init__(self):
    super(UIWidget, self).__init__()
    self.initUI()

  def initUI(self):
    
    #renames the window
    self.setWindowTitle('L-Systems Generator')
    
    #creates the labels for each text box
    self.axiom = QLabel('Axiom')
    self.prodrules = QLabel('Production Rules')
    self.angle = QLabel('Angles(degrees)')
    self.iters = QLabel('Iterations')

    #creates the text box for each label
    self.axiomEdit = QLineEdit()
    self.prodrulesEdit = QLineEdit()
    self.angleEdit = QLineEdit()
    self.itersEdit = QLineEdit()

    #creates a grid for the layout
    grid = QGridLayout()
    grid.setSpacing(20)

    #adds the labels and textboxes into the grid
    grid.addWidget(self.axiom, 1, 0)
    grid.addWidget(self.axiomEdit, 1, 1)

    grid.addWidget(self.prodrules, 2, 0)
    grid.addWidget(self.prodrulesEdit, 2, 1)

    grid.addWidget(self.angle, 3, 0)
    grid.addWidget(self.angleEdit, 3, 1)

    grid.addWidget(self.iters, 4, 0)
    grid.addWidget(self.itersEdit, 4, 1)

    #makes the lsys generator button
    lsysbutton = QPushButton("Generate L System", self)
    grid.addWidget(lsysbutton, 8, 0)
    lsysbutton.clicked.connect(self.genLSys)
    
    #make the exit button
    exitbutton = QPushButton("Exit", self)
    grid.addWidget(exitbutton, 8, 1)
    exitbutton.clicked.connect(exit)

    #loads the grid into the layout
    self.setLayout(grid)


  def genLSys(self):
    axiomInput = self.axiomEdit.text()
    prodInput = self.prodrulesEdit.text()
    angleInput = self.angleEdit.text()
    itersInput = self.itersEdit.text()
    print("Axiom: ", axiomInput)
    print("Productions: ", prodInput)
    print("Angle: ", angleInput)
    print("Iterations: ", itersInput)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UIWidget()
    ui.show()
    sys.exit(app.exec_())

