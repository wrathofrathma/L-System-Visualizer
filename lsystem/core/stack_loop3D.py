"""This module makes the stack loop"""
import math
from time import time

import numpy as np
from scipy.spatial.transform import Rotation as R
def read_substring(
    lsys, curr_state, turn_angle, obj
):
    """
    This is a utility function for read_stack, takes in a string without
    branching ([, ]) or move without draw (f)

    Inputs:
        lsys: a string
        curr_state: a dictionary that has current point, and orientation
        turn_angle: the degrees the angle should turn when seeing a +, -, ^, &, < or >
        obj: the type of object that should be displayed, needs to be a mesh object
    Outputs:
        An array of type obj
    """
    obj_container = []  # make sure it's empty
    current_point = curr_state['point']  # initalize starting point
    #Rotation matrix converts a vector in the abs frame to turtle frame
    vertices = []
    orientation_mat= curr_state['orientation_mat']
    rotation=obj_ortientation = R.from_matrix(orientation_mat)
    vertices.append(current_point)
    #new_obj = obj(pos=current_point,rotation=obj_ortientation.as_rotvec()) # append first object
    #obj_container.append(new_obj)
    '''First row of the rotation matirx is the turtles forward
        direction vector in the absolute frame
        Second row of the rotation matrix is the turtles right
        direction vector in the absolute frame
        Third row of the rotation matrix is the turtles down
        direction vector in the absolute frame
    '''
    unit_step = curr_state['orientation_mat'][0]
    for char in lsys:
        if char == "F":
            old_point = current_point
            current_point = np.add(current_point, unit_step)
            vertices.append(current_point)
            obj_ortientation = R.from_matrix(orientation_mat)
            new_obj = obj(start = old_point, end = current_point, rotation=obj_ortientation.as_rotvec())
            obj_container.append(new_obj)
        elif char == "+":
            #turning left (about the turtle's down axis)
            rotation_vector = np.array(orientation_mat[2])*turn_angle
            rotation=R.from_rotvec(rotation_vector)
            orientation_mat = rotation.apply(orientation_mat)
            unit_step = orientation_mat[0]
        elif char == "-":
            #turning right (about the turtle's down axis)
            rotation_vector = np.array(orientation_mat[2])*turn_angle*(-1)
            rotation=R.from_rotvec(rotation_vector)
            orientation_mat = rotation.apply(orientation_mat)
            unit_step = orientation_mat[0]
        elif char == "<":
            #rolling left (about the turtle's forward axis)
            rotation_vector = np.array(orientation_mat[0])*turn_angle
            rotation=R.from_rotvec(rotation_vector)
            orientation_mat = rotation.apply(orientation_mat)
            unit_step = orientation_mat[0]
        elif char == ">":
            #rolling right (about the turtle's forward axis)
            rotation_vector = np.array(orientation_mat[0])*turn_angle*(-1)
            rotation=R.from_rotvec(rotation_vector)
            orientation_mat = rotation.apply(orientation_mat)
            unit_step = orientation_mat[0]
        elif char == "^":
            #pitch up (about the turtle's right axis)
            rotation_vector = np.array(orientation_mat[1])*turn_angle
            rotation=R.from_rotvec(rotation_vector)
            orientation_mat = rotation.apply(orientation_mat)
            unit_step = orientation_mat[0]
        elif char == "&":
            #pitch down (about the turtle's right axis)
            rotation_vector = np.array(orientation_mat[1])*turn_angle*(-1)
            rotation=R.from_rotvec(rotation_vector)
            orientation_mat = rotation.apply(orientation_mat)
            unit_step = orientation_mat[0]
    curr_state['point'] = current_point
    # returns angle that string left off on, array of vertices, and the new angle
    return orientation_mat, obj_container, vertices


def read_stack(stack, starting_pt, angle, obj):
    """
    This function converts a string into an array of objects placed at the vertices
    determined by the turtle graphics interpretation of the string

    Inputs:
        stack: a string
        starting_pt: the turtles starting_pt (the origin of your fractal)
        angle: the degrees the angle should turn when seeing a +, -, ^, &, < or >
        obj: the type of object that should be displayed, needs to be a mesh object
    Outputs:
        An array of type obj
    """
    angle = angle*np.pi/180
    stack = stack.replace("G", "F")
    stack = stack.replace("g", "f")
    array_of_objects = []
    twoD_array_objects = []
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
    t = time()
    curr_state = {"point": starting_pt, "orientation_mat": np.array([[1, 0, 0],[0,1,0],[0,0,1]])}
    # for each little f/h create a new array with the starting position and angle
    # initialized from the previous mesh
    for char in tmp_stack:
        if char[0] == "f":
            char.replace("f", "")
            unit_step = curr_state['orientation_mat'][0]
            prev_point = curr_state['point']
            curr_state['point'] = np.add(curr_state['point'], unit_step)
            rotation=obj_ortientation = R.from_matrix(curr_state['orientation_mat'])
            new_obj = obj(start=prev_point, end=curr_state['point'], rotation=obj_ortientation.as_rotvec())
        elif char[0] == "[":
            saved_states.append(
                (curr_state["point"], curr_state["orientation_mat"])
            )
            char.replace("[", "")
        elif char[0] == "]":
            tmp_state = saved_states.pop()
            curr_state["point"] = tmp_state[0]
            curr_state["orientation_mat"] = tmp_state[1]
            char.replace("]", "")

        curr_state["orientation_mat"], array_of_objects, verts = read_substring(
            char,
            curr_state,
            angle,
            obj,
        )
        #if not(len(array_of_objects) == 1):
        twoD_array_objects.append(array_of_objects)
        #print(curr_state['point'])
        #curr_state["point"] = verts[-1]
    print("[ INFO ] Finshed finding vertices (", round(time() - t, 3), "s )")
    return twoD_array_objects

# if __name__ == "__main__":
#     str = "FF+F-F{F}"
#     starting_pt=[0,0,0]
#     curr_state = {"point": starting_pt, "angle": np.array([1,0,0], dtype=float), "scale": float(1)}
#     print(read_substring(str, curr_state, np.radians(45)))
