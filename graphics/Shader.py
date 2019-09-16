from OpenGL.GL import (glAttachShader, glCreateShader, GL_LINK_STATUS, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glShaderSource, GL_COMPILE_STATUS, glCompileShader, glCreateProgram, glDeleteShader, glGetAttribLocation, glLinkProgram, glUseProgram)
import numpy as np

class Shader:
    # Input - Filenames to vertex and fragment shader locations.
    def __init__(self, vertex, fragment):
        self.loaded = False
        self.vertex_fname = vertex
        self.fragment_fname = fragment
        # Load filenames to a string
        with open(vertex, "r") as f:
            self.vertex_code = "".join(f.readlines()[1:])
        with open(fragment, "r") as f:
            self.fragment_code = "".join(f.readlines()[1:])
        self.vertex_id = self.createShader(self.vertex_code, GL_VERTEX_SHADER)
        self.fragment_id = self.createShader(self.vertex_code, GL_FRAGMENT_SHADER)
        self.m_program = self.createShaderProgram(self.vertex_id, self.fragment_id)
    # Loads a shader file.
    # Input - string containing shader code, shader type
    # output shader id
    def createShader(self, s, shader_type):
        shader_id = glCreateShader(shader_type)
        glShaderSource(shader_id,s)
        glCompileShader(shader_id)
        self.checkShaderError(shader_id, GL_COMPILE_STATUS, False, "Error compiling shader!")
        return shader_id
    # Binds the shaders together and creates a useable shader program
    def createShaderProgram(self, vertex, frag):
        m_program = glCreateProgram()
        glAttachShader(m_program, vertex)
        glAttachShader(m_program, frag)
        glLinkProgram(m_program)
        self.loaded = self.checkShaderError(m_program, GL_LINK_STATUS, True, "Invalid shader program")
        if(self.loaded):
            pass # Set up uniform variables
        return m_program
    # Binds the shader program for use
    def bind(self):
        pass
    # checks our shader for errors
    def checkShaderError(self, shader_id, flag, isProgram, error_message):
        pass


    # Checks if our shader is loaded and ready for use
    def isLoaded(self):
        pass
    # Gets the id of the shader program
    def getID(self):
        pass

    # Cleans up the shader memory from the graphics card
    def cleanup(self):
        pass
