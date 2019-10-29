from lsystem.graphics.SpatialObject import *

from glm import mat4, vec3, lookAt
from math import cos, sin, pi

class OrbitalObject(SpatialObject):
    def __init__(self):
        super().__init__()
        self.r = 2
        self.theta = 0
        self.psi = 0
        self.deg = pi / 180.0
        self.origin = vec3(0)

    def setPosition(self, r, theta, psi):
        self.r = r
        self.theta = theta
        self.psi = psi
        self.position = vec3(r*cos(psi*self.deg)*cos(theta*self.deg),r*sin(psi*self.deg),r*cos(psi*self.deg)*sin(theta*self.deg))

    def getPosition(self):
        self.position = vec3(self.r*cos(self.psi*self.deg)*cos(self.theta*self.deg),self.r*sin(self.psi*self.deg),self.r*cos(self.psi*self.deg)*sin(self.theta*self.deg))
        return self.position

    def setOrigin(self, origin):
        self.origin = vec3(origin)

    def addTheta(self, num):
        self.theta += num
        if(self.theta > 360):
            self.theta-=360
        if(self.theta<0):
            self.theta+=360
        self.setPosition(self.r, self.theta, self.psi)

    def addR(self,num):
        self.r+=num
        if(self.r<0.000001):
            self.r=0.000001
        self.setPosition(self.r, self.theta, self.psi)

    def addPsi(self,num):
        self.psi+=num
        if(self.psi>90):
            self.psi=90
        if(self.psi<-90):
            self.psi=-90
        self.setPosition(self.r, self.theta, self.psi)

    def setPsi(self, num):
        self.psi=num
        if(self.psi>90):
            self.psi=90
        if(self.psi<-90):
            self.psi=-90
        self.setPosition(self.r, self.theta, self.psi)

    def setR(self, num):
        self.r = num
        if(self.r<0.000001):
            self.r=0.000001
        self.setPosition(self.r, self.theta, self.psi)

    def setTheta(self, num):
        self.num=num
        while(self.theta>360):
            self.theta-=360
        while(self.theta<0):
            self.theta+=360
        self.setPosition(self.r, self.theta, self.psi)

    def getTheta(self):
        return self.theta

    def getR(self):
        return self.r

    def getPsi(self):
        return self.psi

    def getFacing(self):
        eye = vec3(self.r*cos(self.psi*self.deg)*cos(self.theta*self.deg),self.r*sin(self.psi*self.deg),self.r*cos(self.psi*self.deg)*sin(self.theta*self.deg))
        center = self.origin
        up = vec3(0,1,0)
        return lookAt(eye,center,up)
