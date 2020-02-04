import numpy as np

def gen_pixel_map(meshes, size):
  #meshes is an array of arrays of vertices
  #add one and multiply by half of size to get from world coord to pixel map
  pix_map = np.full((size,size),'.')
  meshes = np.asarray(meshes)
  # print(meshes)
  meshes = (meshes)*size
  # print(meshes)
  for vert_array in meshes:
    if len(vert_array) >2:
      #initialize first coordinate pair
      x_old = vert_array[0]
      y_old = vert_array[1]
      #add it to the pixel map
      pix_map[int(np.trunc(x_old)), int(np.trunc(y_old))]=1
      for i in range(2,len(vert_array)-1,2):
        #second coordinate pair
        x_new = vert_array[i] #coordinates are stored as real numbers for precision
        y_new = vert_array[i+1]


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
        x_old = x_new
        y_old = y_new

  print("pixel map done")
  return pix_map
  #np.set_printoptions(threshold=np.inf)
  #print(pix_map)

#TODO: look for predone pooling function
def pool_pixel_map(map):
  size = len(map)
  pix_map = np.full((int(size/2),int(size/2)),'.')
  for i in range(0,size,2):
    for j in range(0,size,2):
      if (map[i,j] == '1' or map[i+1,j]=='1' or map[i,j+1]=='1' or map[i+1,j+1]=='1'):
        pix_map[int(i/2), int(j/2)]=1
  return pix_map

def fractal_dim_calc(meshes):
  size = 512
  pix_map = gen_pixel_map(meshes,size)
  count= 0
  fractal_dim = np.log(np.count_nonzero(pix_map == '1'))/np.log(size)
  return fractal_dim
  # np.set_printoptions(threshold=np.inf)
  # np.set_printoptions(linewidth= np.inf)
  # print(pix_map)

  # print(len(pix_map))
  # pix_map = pool_pixel_map(pix_map)
  # pix_map = pool_pixel_map(pix_map)
  # pix_map = pool_pixel_map(pix_map)
  # pix_map = pool_pixel_map(pix_map)
  # pix_map = pool_pixel_map(pix_map)
  # print(np.array2string(pix_map, separator=',', formatter={'str_kind': lambda x: x}))
  #np.set_printoptions(threshold=np.inf)
  #print(pix_map)
  #print(len(pix_map))
