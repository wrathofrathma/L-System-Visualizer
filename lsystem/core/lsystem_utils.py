""" This file for now is acting as a catch-all utility file."""
import json
import os
import platform
import copy
import logging
from pathlib import Path
import numpy as np
from lsystem.core.parsing import parsed_thread
from lsystem.core.stack_loop import read_stack as read_2d_stack
from lsystem.core.stack_loop3D import read_stack as read_3d_stack
from lsystem.core.graph import Graph
from lsystem.graphics.square import Square
from lsystem.graphics.pipe import Pipe

# At the moment the most important definitions are
# saved_lsystems - Global dictionary definition of loaded lsystems.
# save_lsystem - Save an lsystem to the user defined json file.
# load_saved_lsystems() - Loads the saved & predefined lsystems from file into grammar dictionary.
# get_saved_lsystem(key) - Returns a loaded lsystem from the dictionary.
# generate_lsystem(grammar) - Generates the vertices of a given lsystem
# normalize_coordinates(verts) - Normalizes verts given a numpy array.


# Global dictionary of lsystems.
# The dictionary uses the following keys.
# 'axiom' : string for the axiom
# 'rules' : dict of production rules
# 'angle' : the angle in degrees(integer)
# 'iterations' : number of iterations(integer)
# predefined areas to keep the files.


def get_saved_lsystem(key, saved_lsystems):
    """
    Fetches a saved lsystem in our loaded lsystems by key.

    Parameters:
    key (string): Dictionary key used to identify a saved lsystem.
    saved_lsystems (dict): Dictionary of loaded lsystems.

    Returns:
    dict: dictionary of the saved lsystem grammar, or None if it doesn't exist.
    """
    if key in saved_lsystems:
        grammar = saved_lsystems[key]
        return grammar
    else:
        print("[ ERROR ] No L-System loaded with key: " + str(key))
        return None


def generate_lsystem_2d(grammar):
    """
    Generates a 2D L-System based off of the grammar.

    Parameters:
    grammar (dict): Dictionary representing the grammar defining the lsystem.

    Returns:
    Graph: Graph object used to generate the mesh.
    """
    grammar_copy = copy.deepcopy(grammar)
    graph = Graph()  # Adjacency list based graph.
    print("[ INFO ] Generating L-System with the given grammar..." + str(grammar))
    # Generate full production string.
    tmp_stack = parsed_thread(
        grammar_copy["axiom"], grammar_copy["rules"], grammar_copy["iterations"]
    )
    # Generate vertics
    verts_arr_temp = read_2d_stack(
        tmp_stack,
        [0, 0, 0],
        grammar_copy["angle"],
        grammar_copy["turnAngle"],
        grammar_copy["lineScale"],
    )
    verts_arr_temp = np.array(verts_arr_temp)
    # for now manually strip the x and y values from verts_arr_temp
    x_vals = []
    y_vals = []
    for mesh in verts_arr_temp:
        for point in mesh:
            x_vals.append(point[0])
            y_vals.append(point[1])
    minx = min(x_vals)
    maxx = max(x_vals)
    miny = min(y_vals)
    maxy = max(y_vals)
    maxdif = max([maxx - minx, maxy - miny])
    # Find the min and max of x and y.
    # Find the max of abs(x_max-x_min) and abs(y_max-y_min)
    # Then perform (x-x_min)/max diff * .9999 and (y-y_min)/max diff * .9999

    # Edited for temporary support of adjacency lists. It's wasteful currently, but when we integrate it further back into the tech stack during refactor, it
    # should become more efficient.
    # Since each verts_arr_temp/verts represents an individual fork, we can assume they are connected by edges. So let's track the previous point and draw lines.
    for verts in verts_arr_temp:
        verts = np.array(verts, dtype=np.float32)
        verts = verts.reshape(verts.shape[0] * verts.shape[1])
        for i in range(0, len(verts), 3):  # change this to a 2 to make it 2D
            verts[i] = ((verts[i] - minx) * 0.99999) / maxdif
            verts[i + 1] = ((verts[i + 1] - miny) * 0.99999) / maxdif
            graph.add_vertex((verts[i], verts[i + 1]))
            if i > 0:
                graph.add_edge((prev_point), (verts[i], verts[i + 1]))
            prev_point = (verts[i], verts[i + 1])

    return graph

def generate_lsystem_3d(grammar):
    """
    Generates a 3D L-System based off of the grammar.

    Parameters:
    grammar (dict): Dictionary representing the grammar defining the lsystem.
    """
    grammar_copy = copy.deepcopy(grammar)
    graph = Graph()  # Adjacency list based graph.
    print("[ INFO ] Generating L-System with the given grammar..." + str(grammar))
    # Generate full production string.
    tmp_stack = parsed_thread(
        grammar_copy["axiom"], grammar_copy["rules"], grammar_copy["iterations"]
    )
    # Generate vertics
    mesh = read_3d_stack(
        tmp_stack,
        [0, 0, 0],
        grammar_copy["angle"],
        Pipe
    )

    return mesh

def get_saved_path():
  """Gets the operating system dependent saved_lsystems.json path

  Returns:
  - os.path: Operating system dependent saved_lsystems.json path
  """
  opsys = platform.system()
  if (opsys == 'Linux' or opsys == 'Darwin'):
    path = os.path.join(str(Path.home()), ".config/lsystem")
  elif(opsys=='Windows'):
    path = os.path.expandvars(r'%APPDATA%\lsystem')
  assert path is not None, "Something went wrong parsing operating system platform"
  try:
    os.makedirs(path)
  except FileExistsError:
    pass
  path = os.path.join(path, "saved_lsystems.json")
  return path


def save_lsystem(key, grammar):
    """
    Saves a given lsystem to disk to "lsystem/saved_lsystems.json"
    Overwrites any previous lsystem defined with the same key.

    Parameters:
    key (string): Key used to identify the lsystem.
    grammar (dict): Dictionary of the grammar defining the lsystem.

    Returns:
    - dict: New dictionary of lsystems with the new addition.
    """
    saved_lsystems = {}
    saved_file = get_saved_path()
    # Check if the file exists.
    if os.path.exists(saved_file):
        # If it does, then load all saved data and replace/insert the new data to the dict.
        with open(saved_file, "r") as sfile:
            saved = json.load(sfile)
            saved[key] = grammar
    else:
        # if it doesn't exist, we just create a new dict
        saved = {key: grammar}
    # Then overwrite the file.
    with open(saved_file, "w") as sfile:
        json.dump(saved, sfile, indent=2)
    return saved_lsystems

def load_saved_lsystems():
    """
    Loads the pre-defined and user defined L'Systems.

    Returns:
    - dict: Dictionary of all saved lsystems in the form of {key:grammar, key:grammar}
    """
    saved_lsystems = {}
    saved_file = get_saved_path()
    predef_file = os.path.join(os.path.dirname(__file__), "../assets/lsystems/predefined_lsystems.json")
    print(predef_file)
    print("[ INFO ] Loading saved L-Systems from disk...")
    # Check if the file exists.
    if os.path.exists(predef_file):
        # If it does, then load it as a json object.
        predef = json.load(open(predef_file, "r"))
        # For every key(aka lsystem definition), add it to our saved lsystems.
        for key in predef.keys():
            saved_lsystems[key] = predef[key]

    # Check if the file exists.
    if os.path.exists(saved_file):
        # If it does, then load it as a json object.
        saved = json.load(open(saved_file, "r"))
        # For every key(aka lsystem definition), add it to our saved lsystems.
        for key in saved.keys():
            saved_lsystems[key] = saved[key]
    return saved_lsystems


def remove_saved_lsystem(key):
    """
    Deletes saved lsystem by key by loading the file into a json object, removing the key, then writing the file back to disk.

    Parameters:
    key (string): Key of the lsystem to remove.
    """
    saved_file = "assets/lsystems/saved_lsystems.json"
    # Check if the file exists.
    if os.path.exists(saved_file):
        # If it does, then load all saved data and delete the data, then resave it.
        with open(saved_file, "r") as sfile:
            saved = json.load(sfile)
            try:
                del saved[key]
            except KeyError:
                print("[ ERROR ] Key " + str(key) + " not found in saved lsystems")
    else:
        # if it doesn't exist, we just return
        return
    # Then overwrite the file.
    with open(saved_file, "w") as sfile:
        json.dump(saved, sfile, indent=2)
