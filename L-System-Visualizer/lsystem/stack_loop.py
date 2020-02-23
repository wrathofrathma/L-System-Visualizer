"""This module makes the stack loop"""
import math
from time import time

import numpy as np


def read_substring(
    lsys, starting_pt, start_angle, turn_angle, trig_dict, scale, line_scale
):
    """
    Input: readsubstring takes in a string of the current lsystem,
    a starting point, the starting angle,
    the dictinary of angle trig values,
    current line scale,
    and what the line scale would change by

    Output: returns angle and vertices
    """
    vert_container = []  # make sure it's empty
    new_point = starting_pt  # initalize starting point
    new_angle = start_angle  # initalize starting angle
    vert_container.append(new_point)  # append first point
    for char in lsys:
        if not new_angle in trig_dict.keys():
            trig_dict[new_angle] = [
                math.cos(new_angle * np.pi / 180),
                math.sin(new_angle * np.pi / 180),
            ]
        if char == "F":
            new_point = [
                new_point[0] + (scale * trig_dict[new_angle][0]),
                new_point[1] + (scale * trig_dict[new_angle][1]),
                0,
            ]
            vert_container.append(new_point)
        elif char == "H":
            new_point = [
                new_point[0] + (scale * trig_dict[new_angle][0] / 2),
                new_point[1] + (scale * trig_dict[new_angle][1] / 2),
                0,
            ]
            vert_container.append(new_point)
        elif char == "+":
            new_angle = round((new_angle - trig_dict["angle"]) % 360, 5)
        elif char == "-":
            new_angle = round((new_angle + trig_dict["angle"]) % 360, 5)
        elif char == "|":
            new_angle = round((new_angle + 180) % 360, 5)
        elif char == "(":
            trig_dict["angle"] = round((trig_dict["angle"] - turn_angle) % 360, 5)
            # new_angle = round((new_angle - turn_angle)%360,5)
        elif char == ")":
            trig_dict["angle"] = round((trig_dict["angle"] + turn_angle) % 360, 5)
            # new_angle = round((new_angle + turn_angle)%360,5)
        elif char == ">":
            scale *= line_scale
        elif char == "<":
            scale /= line_scale
    # returns angle that string left off on, array of vertices, and the new angle
    return new_angle, vert_container, scale


def read_stack(stack, starting_pt, angle, turn_angle, line_scale):
    """
    Input list of strings (F, +, -)
    Output List of new vertices
    """
    stack = stack.replace("G", "F")
    stack = stack.replace("g", "f")
    vertices = []
    vert_arr = []
    s = []
    saved_states = []
    # keep the delimeter as the first character of the string
    while len(stack) > 0:
        index_start_b = stack[1:].find("[")  # index of staring bracket
        index_end_b = stack[1:].find("]")  # index of end bracket
        index_f = stack[1:].find("f")  # index of little f
        index_h = stack[1:].find("h")  # index of little h
        if max([index_start_b, index_end_b, index_f, index_h]) == -1:
            s.append(stack)
            stack = []
        else:
            next_break = min(
                i for i in [index_start_b, index_end_b, index_f, index_h] if i >= 0
            )
            s.append(stack[0 : next_break + 1])
            stack = stack[next_break + 1 :]
    # Set up a dictionary of all the possible angles
    # calculate the sin and cos of those angles ahead of time
    # WARNING currently rounding all angles to 5 digits, may not be exact enough

    # trig dict keeps track of the cos and sin of all the angles in radians
    # format trig_dict[an_angle] = [cos(an_angle), sin(an_angle)]
    # trig_dict["angle"] = the user inputted angle
    trig_dict = dict()
    trig_dict["angle"] = angle
    t = time()
    # new_point = starting_pt  # new point initalized to starting point
    curr_state = {"point": starting_pt, "angle": 0, "scale": float(1)}
    print(curr_state["angle"])
    print("TRIG DICT: ", trig_dict)
    # for each little f/h create a new array with the starting position and angle
    # initialized from the previous mesh
    for char in s:
        if char[0] == "f" or char[0] == "h":
            if char[0] == "h":
                divisor = 2
                char.replace("h", "")
            else:
                divisor = 1
                char.replace("f", "")
            if curr_state["angle"] not in trig_dict.keys():
                trig_dict[curr_state["angle"]] = [
                    math.cos(curr_state["angle"] * np.pi / 180),
                    math.sin(curr_state["angle"] * np.pi / 180),
                ]
            curr_state["point"] = [
                curr_state["point"][0]
                + (curr_state["scale"] * trig_dict[curr_state["angle"]][0] / divisor),
                curr_state["point"][1]
                + (curr_state["scale"] * trig_dict[curr_state["angle"]][1] / divisor),
                0,
            ]
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

        curr_state["angle"], vertices, curr_state["scale"] = read_substring(
            char,
            curr_state["point"],
            curr_state["angle"],
            turn_angle,
            trig_dict,
            curr_state["scale"],
            line_scale,
        )
        vert_arr.append(vertices)
        curr_state["point"] = vertices[-1]
    print("[ INFO ] Finshed finding vertices (", round(time() - t, 3), "s )")
    return vert_arr
