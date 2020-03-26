"""This module makes the stack loop"""
import math
from time import time

import numpy as np
from scipy.spatial.transform import Rotation as R
def read_substring(
    lsys, curr_state, turn_angle, scale_factor, obj
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
    new_obj = obj(new_point) # append first object
    obj_container.append(new_obj)
    angle = curr_state['angle']
    for char in lsys:
        if char == "F":
            new_point = np.add(new_point, angle)
            new_obj = obj(new_point)
            obj_container.append(new_obj)
        elif char == "H":
            new_point = np.add(np.mult(new_point,.5), angle)
            new_obj = obj(new_point)
            obj_container.append(new_obj)
        elif char == "+":
            rotation_vector = np.array([0,0,1])*turn_angle #rotate in xy plane
            rotation=R.from_rotvec(rotation_vector)
            rotated_angle = rotation.apply(angle)
            angle = rotated_angle

        elif char == "-":
            rotation_vector = np.array([0,0,-1])*turn_angle #rotate in xy plane
            rotation=R.from_rotvec(rotation_vector)
            rotated_angle = rotation.apply(angle)
            angle = rotated_angle
        elif char == "\\":
            rotation_vector = np.array([1,0,0])*turn_angle #rotate in xy plane
            rotation=R.from_rotvec(rotation_vector)
            rotated_angle = rotation.apply(angle)
            angle = rotated_angle
        elif char == "/":
            rotation_vector = np.array([-1,0,0])*turn_angle #rotate in xy plane
            rotation=R.from_rotvec(rotation_vector)
            rotated_angle = rotation.apply(angle)
            angle = rotated_angle
        elif char == "{":
            rotation_vector = np.array([0,1,0])*turn_angle #rotate in xy plane
            rotation=R.from_rotvec(rotation_vector)
            rotated_angle = rotation.apply(angle)
            angle = rotated_angle
        elif char == "}":
            rotation_vector = np.array([0,-1,0])*turn_angle #rotate in xy plane
            rotation=R.from_rotvec(rotation_vector)
            rotated_angle = rotation.apply(angle)
            angle = rotated_angle
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


def read_stack(stack, starting_pt, angle, turn_angle, scale_factor, obj):
    """
    Input list of strings (F, +, -)
    Output List of new vertices
    """
    print("turn angle at beginning is: ",turn_angle)
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
    curr_state = {"point": starting_pt, "angle": np.array([0, 1, 0], dtype=np.float32), "scale": float(1)}
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
            angle,
            scale_factor,
            obj,
        )
        if len(objs) != 1:
            obj_arr.append(objs)
        curr_state["point"] = objs[-1].opts['position']
    print("[ INFO ] Finshed finding vertices (", round(time() - t, 3), "s )")
    return obj_arr

# if __name__ == "__main__":
#     str = "FF+F-F{F}"
#     starting_pt=[0,0,0]
#     curr_state = {"point": starting_pt, "angle": np.array([1,0,0], dtype=float), "scale": float(1)}
#     print(read_substring(str, curr_state, np.radians(45)))
