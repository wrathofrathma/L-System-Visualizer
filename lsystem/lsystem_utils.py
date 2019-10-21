import lsystem.Lsystem as ls
import lsystem.stack_loop as sl
import math
import numpy as np
import json
import os
import copy
from lsystem.Lsystem import *
from lsystem.stack_loop import *

# This file for now is acting as a catch-all utility file.
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
saved_lsystems = {}
# predefined areas to keep the files.
predef_file = "assets/lsystems/predefined_lsystems.json"
saved_file = "assets/lsystems/saved_lsystems.json"

def generate_lsystem(grammar):
  grammar_copy= copy.deepcopy(grammar)
  print("[ INFO ] Generating L-System with the given grammar..." + str(grammar))
  # Generate full production string.
  s = lThread(grammar_copy['axiom'], grammar_copy['rules'], grammar_copy['iterations'])
  # Generate vertics
  verts_arr_temp = readStack(s,(0,0),grammar_copy['angle'])
  verts_arr = []
  m = map(max,verts_arr_temp)
  m=max(max(m))
  for verts in verts_arr_temp:
    verts = np.array(verts, dtype=np.float32)
    #print(verts)
    rows = len(verts)
    verts = verts.reshape(verts.shape[0]*verts.shape[1])
    verts = normalize_coordinates(verts,m)
    verts_arr.append(verts)
  return verts_arr

# Saves a given lsystem to disk to "lsystem/saved_lsystems.json"
# Overwrites any previous lsystem defined with the same key.
def save_lsystem(key, grammar):
  # Check if the file exists.
  if(os.path.exists(saved_file)):
    # If it does, then load all saved data and replace/insert the new data to the dict.
    with open(saved_file, "r") as sfile:
      saved = json.load(sfile)
      saved[key] = grammar
  else:
    # if it doesn't exist, we just create a new dict
    saved = {key : grammar}
  # Then overwrite the file.
  with open(saved_file,"w") as sfile:
    json.dump(saved, sfile, indent=2)

# Returns a given lsystem's vertices & grammar from the dict. Or returns None.
# The return type is a tuple, (verts, grammar)
# Grammar is a dictionary the represents the axiom, production rules, angle, and iterations to be loaded into the UI.

def get_saved_lsystem(key):
  if key in saved_lsystems:
    grammar = saved_lsystems[key]
    return grammar
  else:
    print("[ ERROR ] No L-System loaded with key: " + str(key))
    return None

# Loads predefined & saved lsystems from file.
def load_saved_lsystems():
  print("[ INFO ] Loading saved L-Systems from disk...")
  # Check if the file exists.
  if(os.path.exists(predef_file)):
    # If it does, then load it as a json object.
    predef = json.load(open(predef_file, "r"))
    # For every key(aka lsystem definition), add it to our saved lsystems.
    for key in predef.keys():
      saved_lsystems[key] = predef[key]

  # Check if the file exists.
  if(os.path.exists(saved_file)):
    # If it does, then load it as a json object.
    saved = json.load(open(saved_file, "r"))
    # For every key(aka lsystem definition), add it to our saved lsystems.
    for key in saved.keys():
      saved_lsystems[key] = saved[key]

# Normalizes the coordinates such that the largest vertice bound is 1 or -1.
# We will remove this later when we have proper scaling/zooming.
def normalize_coordinates(coords,m=0):
  if m == 0:
    m=coords.max()
  coords = coords/m
  return coords
