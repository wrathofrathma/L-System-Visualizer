# This file is for our undirected graph class and helper functions.
# A few notes on the different design decisions here.
# 1. Using a python dictionary with vertices as a key lets us check if vertices exist in much quicker time than doing some_list.index(value).
# 2. Using tuples for vertices allows them to be hashable, aka used as keys in a dict.
# 3. By storing each edge between v1&v2 only once in v1's adjacency_list, we avoid any possible concurrency issues.
# 4. I'm pretty sure we avoid global interpreter lock with this implementation of threading. Will need thorough testing.

from lsystem.graphics.colors import Colors
import threading
from multiprocessing import cpu_count
import numpy as np

class Graph:
  def __init__(self):
    # Vertices will be a dictionary that stores an adjacency list for each vertex.
    self.adjacency_list = {}
    self.colors = []
    self.vertices = []
  # Let's assume the vertex passed is a tuple since that's hashable and we need that for dictionaries to work.
  # Optional color passed for each vertex. Default is white.
  def add_vertex(self, vertex, color=Colors.white):
    if vertex not in self.adjacency_list:
      self.adjacency_list[vertex] = {"edges" : [], "color" : color}
      self.vertices.append(vertex)
      self.colors.append(color)
  # Assume both v1 and v2 are tuples of form (x,y) representing their 2d space position.
  # Normally in undirected graphs you add the edge to both vertices...but we're going to not do that to avoid concurrency issues later.
  # We'll just add to v1 each time.
  def add_edge(self, v1, v2):
    if v1 not in self.adjacency_list:
      self.add_vertex(v1)
    if v2 not in self.adjacency_list:
      self.add_vertex(v2)
    if not self.edge_exists(v1,v2):
      self.adjacency_list[v1]["edges"].append(v2)

  def clear(self):
    self.adjacency_list = {}
    self.colors = []
    self.vertices = []

  # Checks if an edge exists.
  def edge_exists(self, v1, v2):
    if v1 in self.adjacency_list[v2]["edges"] or v2 in self.adjacency_list[v1]["edges"]:
      return True
    return False

# returns a list of tuples that contain ranges for evenly dividing stuff.
# def gen_ranges(n, divs):
#     # filled with tuples for (start,end) values.
#     r = []

#     stride = int(n/divs) # stride is how much we step each iteration
#     offset = 0 # This is our offset for the current iteration.
#     mod = n % divs
#     # If we don't divide evenly, we'll increment by 1 and spread out the extra.
#     if(n % divs!=0):
#         stride+=1
#     for i in range(divs):
#         s = i*stride
#         e = (i+1)*stride
#         # If we're not using our larger stride, then we're offsetting
#         if(i>=mod):
#             s+=offset
#             e+=offset
#         else:
#             offset+=1

#         # Add to our ranges for list comprehension
#         r.append((s,e))
#         if(i==mod-1):
#             stride-=1 # Reset the stride to normal for the rest to evenly divide.
#     return r

# this function will generate vertices,colors, and indices for use in opengl from a graph.
def graph_to_ogl(graph):
  adjacency_list = graph.adjacency_list
  vertices = graph.vertices
  colors = graph.colors
  indices = generate_indices(adjacency_list, vertices)
  # Rejoin all threads.
  v_out = []
  for v in vertices:
    v_out+=v
  c_out = []
  for c in colors:
    c_out += list(c)
  return (np.array(v_out), np.array(c_out), np.array(indices))


# Threaded version of graph_to_ogl
# Since we store each edge exactly once, we can thread safely without concurrency problems, if we thread on each individual vertex.
# So let's divide up the vertices into ranges based on the number of threads we have available.
# def graph_to_ogl(graph):
#     t_num = cpu_count() # Number of threads available

#     vertices = graph.vertices
#     colors = graph.colors

#     adjacency_list = graph.adjacency_list

#     # If we have more threads than we have data, then just reset the number of threads to the data amount.
#     if(len(vertices) < t_num):
#         t_num = len(vertices)
#     t_range = gen_ranges(len(vertices), t_num) # Divides the vertices for each thread to operate on evenly.
#     # Now we have the data split and can use vertices as keys for our dictionary.
#     # It's not perfect, since some vertices have more outgoing edges than others.
#     threads = []

#     # Generate indice output.
#     indices = []
#     for i in range(t_num):
#         indices.append([])

#     # Now let's create a thread for each set of vertices.
#     for i in range(t_num):
#         threads.append(threading.Thread(target=generate_indices, args=(adjacency_list, vertices, t_range[i], i, indices)))
#         threads[i].start()

#     # Rejoin all threads.
#     running=True
#     while(running):
#         running = False
#         for t in threads:
#             if(t.isAlive()):
#                 running=True
#                 break
#     # Generate indices
#     i_out = []
#     for inds in indices:
#         i_out+=inds
#     v_out = []
#     for v in vertices:
#         v_out+=v
#     c_out = []
#     for c in colors:
#         c_out += list(c)
#     return (v_out, c_out, i_out)

def generate_indices(adjacency_list, vert_list):
  # for each vertice in our vertice range
  #   for every outgoing edge
  #       add that line's indice.
  inds = []
  for v in vert_list:
    for e in adjacency_list[v]["edges"]:
      inds += [vert_list.index(v), vert_list.index(e)]
  return inds

# adjacency_list = graph adjacency_list(Graph.vertices)
# vert_list = keys to the adjacency_list
# t_range = range of vertices for the thread to operate on.
# thread_number = thread_number.
# indices
# Tested threaded version fo generate_indices
# def generate_indices(adjacency_list, vert_list, t_range, thread_number, indices):
#     # print("Thread # " + str(thread_number) + " operating on range " + str(t_range))
#     # for each vertice in our vertice range
#     #   for every outgoing edge
#     #       add that line's indice.
#     inds = []
#     for v in vert_list[t_range[0] : t_range[1]]:
#         for e in adjacency_list[v]["edges"]:
#             inds += [vert_list.index(v), vert_list.index(e)]
#     indices[thread_number] += inds
#     # print("Thread #" + str(thread_number) + " terminating")

# g = Graph()
# for i in range(100):
    # g.add_vertex((i,i+1))
# for i in range(10):
    # g.add_edge((i,i+1),(i+1,i+2))
# import numpy as np
# (v,c,i) = graph_to_ogl(g)
# print("Verts: " + str(v))
# print("colors: " + str(c))
# print("Indicies: " + str(i))
