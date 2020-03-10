"""This module makes the stack loop"""
import math
from time import time

import numpy as np
from scipy.spatial.transform import Rotation as R
def read_substring(
    lsys, curr_state, turn_angle,  line_scale, Obj
):
    """
    Input: readsubstring takes in a string of the current lsystem,
    a starting point, the starting angle,
    the dictinary of angle trig values,
    current line scale,
    and what the line scale would change by

    Output: returns angle and vertices
    """
    obj_container = []  # make sure it's empty
    new_point = curr_state['point']  # initalize starting point
    new_obj = Obj(new_point) # append first object
    obj_container.append(new_obj)
    angle = curr_state['angle']
    r1 = R.from_rotvec('z',turn_angle, degrees=True)#for xy plane rotation
    for char in lsys:
        if char == "F":
            new_point = new_point + angle_vector*line_scale
            new_obj = Obj(new_point)
            obj_container.append(new_obj)
        elif char == "H":
            new_point = new_point + angle_vector*.5 *line_scale
            new_obj = Obj(new_point)
            obj_container.append(new_obj)
        elif char == "+":
            change_in_angle = np.array([0,0,1])*turn_angle #rotate in xy plane
            angle = r1.apply(change_in_angle)
        elif char == "-":
            change_in_angle = np.array([0,0,1])*turn_angle*(-1) #rotate in xy plane
            angle = r1.apply(change_in_angle)
        #
        # elif char == "|":
        #     new_angle = round((new_angle + 180) % 360, 5)
        # elif char == "(":
        #     trig_dict["angle"] = round((trig_dict["angle"] - turn_angle) % 360, 5)
        #     # new_angle = round((new_angle - turn_angle)%360,5)
        # elif char == ")":
        #     trig_dict["angle"] = round((trig_dict["angle"] + turn_angle) % 360, 5)
        #     # new_angle = round((new_angle + turn_angle)%360,5)
        # elif char == ">":
        #     curr_state['scale'] *= curr_state['scale']
        # elif char == "<":
        #     curr_state['scale']  /= curr_state['scale']

    # returns angle that string left off on, array of vertices, and the new angle
    return angle, obj_container


def read_stack(stack, starting_pt, angle, turn_angle, line_scale, Obj):
    """
    Input list of strings (F, +, -)
    Output List of new vertices
    """


    stack = stack.replace("G", "F")
    stack = stack.replace("g", "f")
    objs = []
    obj_arr = []
    tmp_stack = []
    saved_states = []
    # keep the delimeter as the first character of the string
    while len(stack) > 0:
        index_start_b = stack[1:].find("[")  # index of staring bracket
        index_end_b = stack[1:].find("]")  # index of end bracket
        index_f = stack[1:].find("f")  # index of little f
        index_h = stack[1:].find("h")  # index of little h
        if max([index_start_b, index_end_b, index_f, index_h]) == -1:
            tmp_stack.append(stack)
            stack = []
        else:
            next_break = min(
                i for i in [index_start_b, index_end_b, index_f, index_h] if i >= 0
            )
            tmp_stack.append(stack[0 : next_break + 1])
            stack = stack[next_break + 1 :]
    # Set up a dictionary of all the possible angles
    # calculate the sin and cos of those angles ahead of time
    # WARNING currently rounding all angles to 5 digits, may not be exact enough

    # trig dict keeps track of the cos and sin of all the angles in radians
    # format trig_dict[an_angle] = [cos(an_angle), sin(an_angle)]
    # trig_dict["angle"] = the user inputted angle
    #trig_dict = dict()
    #trig_dict["angle"] = np.array([0,1,0])
    t = time()
    # new_point = starting_pt  # new point initalized to starting point
    curr_state = {"point": starting_pt, "angle": np.array([0,1,0], dtype=float32), "scale": float(1)}
    print(curr_state["angle"])
    #print("TRIG DICT: ", trig_dict)
    # for each little f/h create a new array with the starting position and angle
    # initialized from the previous mesh
    for char in tmp_stack:
        if char[0] == "f" or char[0] == "h":
            if char[0] == "h":
                divisor = 2
                char.replace("h", "")
            else:
                divisor = 1
                char.replace("f", "")
            curr_state["point"] += curr_state['angle']/divisor
        elif char[0] == "[":
            saved_states.append(
                (curr_state["point"], curr_state["angle"], curr_state["scale"])
            )
            char.replace("[", "")
        elif char[0] == "]":
            tmp_state = saved_states.pop()
            curr_state["point"] = tmp_state[0]
            curr_state["angle"] = tmp_state[1]
            curr_state["scale"] = tmp_state[2]
            char.replace("]", "")

        curr_state["angle"], objs = read_substring(
            char,
            curr_state,
            turn_angle,
            line_scale,
            Obj,
        )
        if len(obj) != 1:
            obj_arr.append(objs)
        curr_state["point"] = obj[-1].opts['position']
    print("[ INFO ] Finshed finding vertices (", round(time() - t, 3), "s )")
    return obj_arr
