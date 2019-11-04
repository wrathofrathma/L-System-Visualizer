# Python core includes 
from PIL import Image
from time import time
# PyQt includes 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
# OpenGL includes 
from OpenGL.GL import shaders
from OpenGL.GL import *
from OpenGL.arrays import ArrayDatatype, vbo
# Lsystem includes 
from lsystem.graphics.Mesh import *
from lsystem.lsystem_utils import *
from lsystem.graphics.SphericalCamera import *
from lsystem.graphics.FreeCamera import *
from lsystem.graphics.RayCasting import *
from lsystem.graphics.Axis import *
from lsystem.graphics.Grid import Grid2D
from lsystem.graphics.colors import Colors
# Other includes 
import numpy as np


# Legit just an enumeration for determining camera type in a readable manner.
class CameraType:
    Free = 0
    Orbital = 1

# PyQt5 widget for displaying L-Systems. 
class LSystemDisplayWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(LSystemDisplayWidget, self).__init__(parent)
        # Background color
        self.bgcolor = Colors.black
        # Time, used for calculating delta time between frames(useful for shader calcs we might want later)
        self.start_time = time()
        
        # Production scene objects. 
        self.meshes = [] # Mesh container should be outdated soon!
        self.grid = Grid2D() # 2D Intersection grid 

        # Camera initialization
        self.cameras = [ FreeCamera(800,600), SphericalCamera(800,600)] # We have both an  oribtal camera and a free camera.
        self.cameras[1].r = 2 # Radius from the origin of the spherical camera. 

        # FLAGS & Defaults 
        self.keep_centered = True # Boolean flag for whether to center the mesh after the viewport resizes.
        self.active_camera = CameraType.Free  # active_camera tracks which index of the camera to use. 
        self.active_shader = None # Tracks which shader to use, 2D vs 3D typically.
        self.dimensionality = 2 # Dimensionality of the LSystem being displayed....probably will get rid of this later?
        self.mesh_options = MeshOptions.White | MeshOptions.Static # Default mesh options are white and static
        self.fps=30.0 # Number of times a second we refresh the widget. 
        self.DISPLAY_GRID=True # Toggles the display of the intersection grid. 

        # DEBUG Flags 
        self.DEBUG=True # Toggles the origin axis & plane & raycasting view. Later it'll toggle other debug utils.
        
        # DEBUG Objects
        # 3D Axis & a plane mesh for visual clarity while I implement zooming into a point.
        # World origin axis
        self.axis = Axis() 
        # Intersecting plane view for when we raycast into the mesh to deterine where to zoom into.
        self.plane = Mesh(3)
        pv = np.array([
        -1, -1, 0,
        -1, 1, 0,
        1, 1, 0,
        1, -1, 0,
        -1, -1, 0
        ], dtype=np.float32)
        self.plane.set_vertices(pv)
        self.plane.translate([0.5,0,0])
        # Axis for camera origin. 
        self.origin_axis = Axis()
        self.origin_axis.scale(0.03)
        # Raycasting ray visualization.
        self.casted_ray = Mesh(3)
        rv = np.array([0,0,0,1,0,0])
        self.casted_ray.set_vertices(rv)
        self.casted_ray.translate([0.5,0,0])

        # threaded timer that refreshes the opengl widget. without this it only updates when we click or trigger an event.
        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1/self.fps)

    # Will toggle the camera type & handle the positional relocating here later when we do live toggle.
    def toggle_camera_type(self):
        self.active_camera = CameraType.Orbital if self.active_camera==CameraType.Free else CameraType.Free
    # Toggle drawing of debug objects.
    def toggle_debug(self):
        self.DEBUG = not self.DEBUG
    # Will return an integer camera type
    def get_camera_type(self):
        return self.active_camera
    # Will accept a CameraType argument(or an integer)
    # 0 = free camera with drag panning
    # 1 = oribtal camera
    def set_camera_type(self,c):
        if(self.active_camera!=c):
            self.toggle_camera_type()
            self.active_camera = c # Fuck error checking
    # Do I really need this? Meh. I was feeling it before but now it feels fat.
    def setDimensions(self, d):
        if(d!=2 and d!=3):
            print("[ ERROR ] Dimensionality being set to something other than 2d or 3d.")
        self.dimensionality=d
        if(d==2):
            self.active_shader=self.shader2D
        else:
            self.active_shader=self.shader3D

    # This is from QOpenGLWidget, this is where all drawing is done.
    def paintGL(self):
        glClearColor(self.bgcolor[0], self.bgcolor[1], self.bgcolor[2], self.bgcolor[3])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Update the camera data
        self.cameras[self.active_camera].update()
        # Upload the updates to both shaders.
        self.cameras[self.active_camera].applyUpdate(self.shader2D)
        self.cameras[self.active_camera].applyUpdate(self.shader3D)
        # Update the shader uniform variables.
        glUseProgram(self.shader2D)
        glUniform1f(glGetUniformLocation(self.shader2D, "time"), time()-self.start_time)
        if(self.mesh_options & MeshOptions.Pulse):
            glUniform1i(glGetUniformLocation(self.shader2D, "pulse"), True)
        else:
            glUniform1i(glGetUniformLocation(self.shader2D, "pulse"), False)

        glUseProgram(self.shader3D)
        glUniform1f(glGetUniformLocation(self.shader3D, "time"), time()-self.start_time)
        # Draw debug objects 
        if(self.DEBUG):
            self.axis.draw()
            self.plane.draw()
            self.origin_axis.draw()
            self.casted_ray.draw()
        if(self.DISPLAY_GRID):
            self.grid.draw()
        # Draw the meshes. TODO - Move this to a graph object later.
        for mesh in self.meshes:
            mesh.draw()


    # Converts a qt mouse position event coordinates to opengl coordinates
    # aka top left from(0,0) to bottom left being (-1,-1) and top right being (1,1)
    def qtPosToOGL(self, pos):
        # Subtract 1/2 the screen w/h from the pos.
        qpos = np.array([pos.x(), pos.y()])
        wsize = np.array([self.size().width(), self.size().height()])
        return qpos - wsize

    # Sets the mesh options.
    def set_mesh_options(self, options):
        # We can use bitwise OR to set the options then XOR to unset the
        if(options & MeshOptions.Colors):
            self.mesh_options = self.mesh_options | MeshOptions.Colors
            if(self.mesh_options & MeshOptions.White):
                self.mesh_options = self.mesh_options ^ MeshOptions.White
        elif(options & MeshOptions.White):
            self.mesh_options = self.mesh_options | MeshOptions.White
            if(self.mesh_options & MeshOptions.Colors):
                self.mesh_options = self.mesh_options ^ MeshOptions.Colors

        if(options & MeshOptions.Static):
            self.mesh_options = self.mesh_options | MeshOptions.Static
            if(self.mesh_options & MeshOptions.Pulse):
                self.mesh_options = self.mesh_options ^ MeshOptions.Pulse

        elif(options & MeshOptions.Pulse):
            self.mesh_options = self.mesh_options | MeshOptions.Pulse
            if(self.mesh_options & MeshOptions.Static):
                self.mesh_options = self.mesh_options ^ MeshOptions.Static


    # Not sure if we'll ever need these NDC conversions, but prepping.
    # Converts a mouse position to normalized device coordinates. Assumes the pos is a tuple, list, or np array of size 2.
    def toNormalizedDeviceCoordinates(self, pos):
        wsize = np.array([self.size().width(), self.size().height()])
        return (pos[0] / wsize[0]*2-1, 1-pos[1]/wsize[1]*2)

    # Converts a Qt event to normalized device coordinates.
    def qtPosToNDC(self, pos):
        qpos = np.array([pos.x(), pos.y()])
        return self.toNormalizedDeviceCoordinates(qpos)

    def zoomIN(self):
        if(self.active_camera==CameraType.Orbital):
            self.cameras[self.active_camera].addR(-0.2)
            print("Radius: " + str(self.cameras[self.active_camera].getR()))
        else:
            self.cameras[self.active_camera].translate([0,0,-0.2])
        self.update()

    def zoomOUT(self):
        if(self.active_camera==CameraType.Orbital):
            self.cameras[self.active_camera].addR(0.2)
            #print("Camera Z coord "+str(self.cameras[self.active_camera].position[2]))
            print("Radius: " + str(self.cameras[self.active_camera].getR()))
        else:
            self.cameras[self.active_camera].translate([0,0,0.2])
        self.update()

    # Resets camera to default position & orientation
    def resetCamera(self):
        if(self.active_camera==CameraType.Orbital):
            self.cameras[self.active_camera].theta = 90
            self.cameras[self.active_camera].psi = 0
            self.cameras[self.active_camera].r = 2
        else:
            self.cameras[self.active_camera].setPosition([0,0,1])
            self.cameras[self.active_camera].setOrientation([0,0,0])
        self.update()

    # Triggered only when the mouse is dragged in the opengl frame with the mouse down(on my machine)
    # We store hte mouse position here, to be used in teh mouse move event.
    def mousePressEvent(self, event):
        self.mouse_last_x = event.pos().x()
        self.mouse_last_y = event.pos().y()
        print("(%s,%s)" % (self.mouse_last_x, self.mouse_last_y))
        print("NDC %s" % (str(self.qtPosToNDC(event.pos()))))
        if(event.button()==Qt.RightButton and self.active_camera==CameraType.Orbital):
            if(self.DEBUG):
                ray = getMouseRaycast(self.qtPosToNDC(event.pos()), self.cameras[self.active_camera].getProjection(), self.cameras[self.active_camera].getView())
                ray-=self.cameras[self.active_camera].position
                self.casted_ray.set_vertices(np.array([self.cameras[self.active_camera].position[0], self.cameras[self.active_camera].position[1], self.cameras[self.active_camera].position[2], ray[0],ray[1],ray[2]]))
                #origin = ray - self.cameras[self.active_camera].getR()
                print("Raycast dir: " + str(ray))
                print("CAmera coordinates: " + str(self.cameras[self.active_camera].position))
                print("Camera R: " + str(self.cameras[self.active_camera].getR()))
                #self.cameras[self.active_camera].setOrigin(origin)

    def mouseMoveEvent(self, event):
        # Store current mouse position
        self.mouse_x = event.pos().x()
        self.mouse_y = event.pos().y()

        # Find the mouse delta
        xdiff = (self.mouse_last_x-self.mouse_x)
        ydiff = (self.mouse_last_y-self.mouse_y)

        if(self.active_camera==CameraType.Orbital): 
            # Get the radius
            radius = self.cameras[self.active_camera].getR()

            self.cameras[self.active_camera].addTheta(xdiff)
            self.cameras[self.active_camera].addPsi(ydiff)
        else:
            # Pan around the scene
            movement_speed = 0.01
            trans_vector = np.zeros(3)
            if(xdiff!=0):
                trans_vector[0] = -1 if xdiff<0 else 1
            if(ydiff!=0):
                trans_vector[1] = 1 if ydiff<0 else -1
            trans_vector*=movement_speed
            
            self.cameras[self.active_camera].translate(trans_vector)
        self.update()
        self.mouse_last_x = self.mouse_x
        self.mouse_last_y = self.mouse_y

    # Called when the OpenGL widget resizes.
    def resizeGL(self, w, h):
        print("[ INFO ] OpenGL Resized: " + str(w) + "," + str(h))
        glViewport(0,0,w,h)
        self.cameras[self.active_camera].resize(w,h)

        if(self.keep_centered):
            self.center_mesh()

    # Defines whether to keep the mesh centered in the view after resizes.
    def center_on_resize(self, val):
        self.keep_centered = val

    # OpenGL initialization
    def initializeGL(self):
        print("[ INFO ] Initializing OpenGL...")
        self.loadShaders()
        print("[ INFO ] Shader ID: " + str(self.active_shader))
    #    glLineWidth(5)
        # Set the shader for every mesh
        self.axis.set_shader(self.shader3D)
        self.origin_axis.set_shader(self.shader3D)
        self.casted_ray.set_shader(self.shader3D)
        self.plane.set_shader(self.shader3D)
        self.grid.set_shader(self.shader2D)
        for mesh in self.meshes:
            mesh.set_shader(self.active_shader)

    def loadShaders(self):
        # Load the shader files into a string.
        print("[ INFO ] Loading shaders...")
        with open("assets/shaders/2DShader.vs","r") as f:
            vc = "".join(f.readlines()[0:])
        with open("assets/shaders/2DShader.fs","r") as f:
            fc = "".join(f.readlines()[0:])

        print("[ INFO ] Loaded 2D shader code...")
        try:
            # Compile hte shaders on the graphics card.
            self.vs2 = shaders.compileShader(vc, GL_VERTEX_SHADER)
            self.fs2 = shaders.compileShader(fc, GL_FRAGMENT_SHADER)
            # Link them together & compile them as a program.
            self.shader2D = shaders.compileProgram(self.vs2, self.fs2)

        except Exception as err:
            print("[ ERROR ] Caught an exception: " + str(err))
            exit(1) # Can't proceed without working shaders.

        # 3D Shaders
        with open("assets/shaders/3DShader.vs","r") as f:
            vc = "".join(f.readlines()[0:])
        with open("assets/shaders/3DShader.fs","r") as f:
            fc = "".join(f.readlines()[0:])
        print("[ INFO ] Loaded 3D shader code...")
        try:
            # Compile hte shaders on the graphics card.
            self.vs3 = shaders.compileShader(vc, GL_VERTEX_SHADER)
            self.fs3 = shaders.compileShader(fc, GL_FRAGMENT_SHADER)
            # Link them together & compile them as a program.
            self.shader3D = shaders.compileProgram(self.vs3, self.fs3)

        except Exception as err:
            print("[ ERROR ] Caught an exception: " + str(err))
            exit(1) # Can't proceed without working shaders.
        self.active_shader=self.shader2D
        print("[ INFO ] Shaders loaded to graphics card.")

    # Saves a screenshot of the current OpenGL buffer to a given filename.
    # MUST have a file extension for now.
    def screenshot(self, filename):
        print("[ INFO ] Saving screenshot to filename " + str(filename) + "...")
        size = self.size()
        pos_x = self.pos().x() # Starts from the left. Which is fine.
        pos_y = self.pos().y() # Starts from the top...so we need to convert this to start from the bottom.
        # So it should be...parent_size - pos_y + open_gl_height
        # Going to do some ghetto stuff and pray the parent is always the  top-level, or else this won't work.
        parent = self.parentWidget()
        pheight = parent.size().height()
        pos_y += size.height()
        pos_y = pheight - pos_y

        # Read all of the pixels into an array.
        pixels = glReadPixels(pos_x,pos_y, size.width(), size.height(), GL_RGB, GL_UNSIGNED_BYTE)
        # Create an image from Python Image Library.
        image = Image.frombytes("RGB", (size.width(), size.height()), pixels)
        # FLip that bitch.
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save(filename)
        print("[ INFO ] Saved.")

    # Cleanups all shader memory & mesh data.
    def cleanup(self):
        print("[ INFO ] Cleaning up display widget memory.")

        # Cleaning up mesh memory on GPU
        self.clear_mesh()

        # Detaching shaders and deleting shader program
        #glDetachShader(self.shader, self.vs)
        #glDetachShader(self.shader, self.fs)
        glDeleteShader(self.vs2)

        glDeleteShader(self.fs2)
        glDeleteProgram(self.shader2D)
        glDeleteShader(self.vs3)

        glDeleteShader(self.fs3)
        glDeleteProgram(self.shader3D)
    # Centers the mesh in the view
    def center_mesh(self):
        # Well, since we have multiple meshes, we need the mins and maxes of all of them before slicing.
        if(len(self.meshes)==0):
            return
        maxes=[]
        mins= []
        for mesh in self.meshes:
            ma, mi = mesh.detect2DEdges()
            maxes.append(ma)
            mins.append(mi)
        # this should create 2, (n,2) dimension numpy arrays.
        maxes = np.array(maxes)
        mins = np.array(mins)
        max_x = maxes[:,0].max()
        max_y = maxes[:,1].max()
        min_x = mins[:,0].min()
        min_y = mins[:,1].min()

        print("Min_x: %3.2f, Max_x: %3.2f, Min_y: %3.2f, Max_y: %3.2f" % (min_x, max_x,min_y, max_y))

    # Sets the vertices of the last mesh in the array.
    # split=True creates a new mesh before setting the vertices.
    def set_vertices(self, vertices, split=False):
        if(split):
            self.meshes.append(Mesh())
            self.meshes[-1].set_shader(self.active_shader)

        self.meshes[-1].set_vertices(vertices)
        self.meshes[-1].set_options(self.mesh_options)

    # Cleans up the mesh memory on the GPU and clears the array of them.
    def clear_mesh(self):
        for mesh in self.meshes:
            mesh.cleanup()
        self.meshes.clear()
        self.meshes.append(Mesh())
        self.meshes[-1].set_shader(self.active_shader)

    # Sets the background color of the OpenGL widget.
    def set_bg_color(self, color):
        if(len(color)==4):
            self.bgcolor = np.array(color, dtype=np.float32)
        elif(len(color==3)):
            self.bgcolor = np.array(color[0], color[1], color[2], 0.0, dtype=np.float32)
        else:
            print("")
        self.bgcolor = color


if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()

    l1 = QLabel('Label 1')
    l2 = QLabel('Label 2')
    ogl = LSystemDisplayWidget()
    layout.addWidget(ogl)

    window.setLayout(layout)
    window.show()

    app.exec_()
    ogl.cleanup()
