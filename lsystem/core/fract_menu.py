'''This file handles the saving of rules'''
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
import numpy as np
import copy

class FractalDimension(QWidget):
    '''Makes the window that allows the user to save rules'''
    def __init__(self, ui):
        '''Initing the name of the box and the ui'''
        super().__init__()
        self.ui = ui
        # creates the widgets to be added to the window
        self.instructions = QLabel("Welcome to the fractal dimension calculator. We calculate based on powers of 2.")
        self.start_prompt = QLabel("Start Power: ")
        self.start_size = QLineEdit()
        self.end_prompt = QLabel("End Power: ")
        self.end_size = QLineEdit()
        self.iters_prompt = QLabel("Number of calculations")
        self.iters_num = QLineEdit()
        self.calc_button = QPushButton("Calculate")
        self.calc_button.clicked.connect(lambda: self.calc())

        self.init_ui()

    def init_ui(self):
        """sets the window title, layout, and adds widgets to the window"""
        self.setWindowTitle("Fractal Dimmension Calculator")
        self.layout = QGridLayout()
        self.add_widgets()
        self.setLayout(self.layout)

    def add_widgets(self):
        '''Adds the widgets to the layout'''
        # adds the widgets to the window
        self.layout.addWidget(self.instructions, 0, 0, 1, 5)
        self.layout.addWidget(self.start_prompt, 2, 0)
        self.layout.addWidget(self.start_size, 2, 1, 1, 2)
        self.layout.addWidget(self.end_prompt, 3, 0)
        self.layout.addWidget(self.end_size, 3, 1, 1, 2)
        self.layout.addWidget(self.iters_prompt, 4, 0)
        self.layout.addWidget(self.iters_num, 4, 1, 1, 2)
        self.layout.addWidget(self.calc_button, 5, 3)

    def calc(self):
      all_dims = []
      for i in range(int(self.iters_num.text())):
        self.ui.gen_sys()
        verts = copy.deepcopy(self.ui.verts)
        fractal_dim = []
        fract_avg = []
        x_arr = []
        y_arr = []

        start = 2 ** int(self.start_size.text())
        end = 2 ** int(self.end_size.text())

        print("Lela's code", verts)
        print("Start size = {}".format(self.start_size.text()))
        print("End size = {}".format(self.end_size.text()))

        pix_map = gen_pixel_map(verts, end)
        fractal_dim.insert(0, np.log2(np.count_nonzero(pix_map == '1')))
        while(end >= start):
            print("LELAS FRACT CALC END STATE", end)
            end = end/2
            pix_map = pool_pixel_map(pix_map)

            fractal_dim.insert(0, np.log2(np.count_nonzero(pix_map == '1')))


        for i, dim in enumerate(fractal_dim):
          x_arr.append(np.log2(start))
          y_arr.append(dim)
          start = start*2
        all_dims.append(np.polyfit(x_arr, y_arr, 1)[0])
      print(all_dims)
          


def gen_pixel_map(graph, size):
  #meshes is an array of arrays of vertices
  #add one and multiply by size to get from world coord to pixel map
  pix_map = np.full((size,size),'.')

  for point in graph.adjacency_list.keys():
    #second coordinate pair
    #print("point = ",point)
    x_old = point[0]*size #coordinates are stored as real numbers for precision
    y_old = point[1]*size
    pix_map[int(np.trunc(x_old)), int(np.trunc(y_old))]=1
    for point2 in graph.adjacency_list[point]["edges"]:
      #print("point 2 = ",point2)
      x_new = point2[0]*size
      y_new = point2[1]*size

      #add the line connection new point and old point
      h=0
      step_size=1/(max(abs(x_new-x_old), abs(y_new-y_old))*2)
      for h in np.arange(0,1,step_size):
        xx = x_old + h*(x_new-x_old)
        yy = y_old + h*(y_new-y_old)
        xx_coord = min(int(np.trunc(xx)),size-1)
        yy_coord = min(int(np.trunc(yy)),size-1)
        pix_map[xx_coord, yy_coord]=1
      #This takes care of edge case where max =1024 is outside of array
      x_new_coord = min(int(np.trunc(x_new)), size-1)
      y_new_coord = min(int(np.trunc(y_new)),size-1)

      pix_map[x_new_coord, y_new_coord]=1
    #x_old = x_new
    #y_old = y_new

  #print("pixel map done")
  return pix_map
  #np.set_printoptions(threshold=np.inf)
  #print(pix_map)
def pool_pixel_map(map):
  size = len(map)
  pix_map = np.full((int(size/2),int(size/2)),'.')
  for i in range(0,size,2):
    for j in range(0,size,2):
      if (map[i,j] == '1' or map[i+1,j]=='1' or map[i,j+1]=='1' or map[i+1,j+1]=='1'):
        pix_map[int(i/2), int(j/2)]=1
  return pix_map
def fractal_dim_calc(graph,ending_size, num_sizes):

  fractal_dim = []
  pix_map = gen_pixel_map(graph,ending_size)
  np.set_printoptions(threshold=np.inf, linewidth = 2000)


  count= 0
  fractal_dim.insert(0,np.log2(np.count_nonzero(pix_map == '1')))#/np.log(ending_size))
  for i in range(num_sizes-1):
    print("STEPHS FRACT_CALC", ending_size)
    ending_size = ending_size/2
    
    pix_map = pool_pixel_map(pix_map)
    #if >2:
    #  print(pix_map)
    fractal_dim.insert(0,np.log2(np.count_nonzero(pix_map == '1')))#/np.log(ending_size))

  return fractal_dim # JUST RETURNS log(N(E))

