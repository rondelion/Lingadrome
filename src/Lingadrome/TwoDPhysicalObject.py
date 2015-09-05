'''
Created on 2015/09/05

@author: rondelion
'''

class TwoDPhysicalObject(object):
    '''
    classdocs
    '''
    __mass=1.0            # Mass (kg)
    __radius=0.1          # Radius (m)
    __staticCOF=1.0       # Static Coefficient of Friction
    __kineticCOF=1.0      # Kinetic Coefficient of Friction
    __location=(0.0,0.0)  # Object location (meter^2)
    __orientation=0.0     # radian
    __velocity=0.0        # m/s
    __acceleration=0.0    # m/s^2
    __angularVelocity=0.0 # radian/s

    def __init__(self, mass=1, kineticCOF=1, staticCOF=1):
        '''
        Constructor
        '''
        self.__mass=mass
        self.__kineticCOF=kineticCOF
        self.__staticCOF=staticCOF
        
    def getMass(self):
        return(self.__mass)
    
    def setMass(self, mass):
        self.__mass = mass
        
    def getRadius(self):
        return(self.__radius)
    
    def setRadius(self, radius):
        self.__radius = radius
        
    def getStaticCOF(self):
        return(self.__staticCOF)
    
    def setStaticCOF(self, staticCOF):
        self.__staticCOF = staticCOF

    def getKineticCOF(self):
        return(self.__kineticCOF)
    
    def setKineticCOF(self, kineticCOF):
        self.__kineticCOF = kineticCOF

    def getLocation(self):
        return(self.__location)
    
    def setLocation(self, location):
        self.__location = location

    def getOrientation(self):
        return(self.__orientation)
    
    def setOrientation(self, orientation):
        self.__orientation = orientation

    def getVelocity(self):
        return(self.__velocity)
    
    def setVelocity(self, velocity):
        self.__velocity = velocity

    def thrust(self, force, time):
        if self.__velocity==0.0 and force<=self.__staticCOF:
                self.__acceleration = 0
        else:
            if force>0:
                self.__acceleration = force/self.__mass - self.__kineticCOF
            else:
                self.__acceleration = force/self.__mass + self.__kineticCOF
        # TODO: Collision handling?
        