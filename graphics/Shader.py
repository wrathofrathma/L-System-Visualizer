from OpenGL.GL import (glAttachShader, glDeleteProgram, glDetachShader, GL_TRUE, glGetProgramiv, glGetProgramInfoLog, glGetShaderInfoLog, GL_FALSE, glCreateShader, glGetShaderiv, GL_LINK_STATUS, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glShaderSource, GL_COMPILE_STATUS, glCompileShader, glCreateProgram, glDeleteShader, glGetAttribLocation, glLinkProgram, glUseProgram)
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
        print("Length of vertex code: " + str(len(self.vertex_code)))
        print("Length of frag code: " + str(len(self.fragment_code)))
        self.vertex_id = self.createShader(self.vertex_code, GL_VERTEX_SHADER)
        self.fragment_id = self.createShader(self.fragment_code, GL_FRAGMENT_SHADER)
        self.m_program = self.createShaderProgram(self.vertex_id, self.fragment_id)
    # Loads a shader file.
    # Input - string containing shader code, shader type
    # output shader id
    def createShader(self, s, shader_type):
        shader_id = glCreateShader(shader_type)
        glShaderSource(shader_id,s)
        glCompileShader(shader_id)
        if(self.checkShaderError(shader_id, GL_COMPILE_STATUS, False, "Error compiling shader!")):
            return shader_id
        else:
            glDeleteShader(shader_id)
            raise RuntimeError("Issue with the shader creation")
    # Binds the shaders together and creates a useable shader program
    def createShaderProgram(self, vertex, frag):
        m_program = glCreateProgram()
        glAttachShader(m_program, vertex)
        glAttachShader(m_program, frag)
        glLinkProgram(m_program)
        self.loaded = self.checkShaderError(m_program, GL_LINK_STATUS, True, "Invalid shader program")
        if(self.loaded):
             # Set up uniform variables
            return m_program
        else:
            glDetachShader(m_program, self.vertex_id)
            glDeleteShader(self.vertex_id)
            glDetachShader(m_program, self.fragment_id)
            glDeleteShader(self.fragment_id)
            glDeleteProgram(m_program)
            raise RuntimeError("Issue linking the shader together")
            return None

    # Binds the shader program for use
    def bind(self):
        glUseProgram(self.m_program)

    # checks our shader for errors
    def checkShaderError(self, shader_id, flag, isProgram, error_message):
        if(isProgram):
            print("Checking program errors")
            if(glGetProgramiv(shader_id, flag)!=GL_TRUE):
                print(glGetProgramiv(shader_id, flag))
                info = glGetProgramInfoLog(shader_id)
                print(error_message + " : " + info)
                return False
        else:
            print("Checking shader errors")
            if(glGetShaderiv(shader_id, flag)!=GL_TRUE):
                print(glGetShaderiv(shader_id, flag))

                info = glGetShaderInfoLog(shader_id)
                print(error_message + " : " + info)
                return False
        return True


    def getUniformLocation(self, s):
        return glGetUniformLocation(self.m_program, s)

    # Checks if our shader is loaded and ready for use
    def isLoaded(self):
        return self.loaded

    # Gets the id of the shader program
    def getID(self):
        if(self.loaded):
            return self.m_program
        else:
            return 0

    # Cleans up the shader memory from the graphics card
    def cleanup(self):
        glDetachShader(self.m_program, self.vertex_id)
        glDeleteShader(self.vertex_id)
        glDetachShader(self.m_program, self.fragment_id)
        glDeleteShader(self.fragment_id)
        glDeleteProgram(self.m_program)
