from PyQt5.QtWidgets import QWidget, QLineEdit, QTextEdit, QGridLayout, QApplication, QLabel
import sys

class GUI(QWidget):
  
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    axiom = QLabel('Axiom')
    prodrules = QLabel('Production Rules')
    angles = QLabel('Angles(degrees)')
    iters = QLabel('Iterations')

    axiomEdit = QLineEdit()
    prodrulesEdit = QLineEdit()
    anglesEdit = QLineEdit()
    itersEdit = QLineEdit()

    grid = QGridLayout()
    grid.setSpacing(20)

    grid.addWidget(axiom, 1, 0)
    grid.addWidget(axiomEdit, 1, 1)

    grid.addWidget(prodrules, 2, 0)
    grid.addWidget(prodrulesEdit, 2, 1)

    grid.addWidget(angles, 3, 0)
    grid.addWidget(anglesEdit, 3, 1)

    grid.addWidget(iters, 4, 0)
    grid.addWidget(itersEdit, 4, 1)

    self.setLayout(grid)

    self.setWindowTitle('L-Systems Generator')
    self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = GUI()
    sys.exit(app.exec())

