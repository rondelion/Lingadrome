'''
Created on 2015/08/28

@author: rondelion
'''

class WorldObject(object):
    '''
    classdocs
    '''
    __location=(0.0,0.0)  # Object location (meter^2)
    __orientation=0.0     # π radian
    __mass=1.0            # Mass
    __staticCOF=1.0       # Static Coefficient of Friction
    __kineticCOF=1.0      # Kinetic Coefficient of Friction
    __direction=0.0       # Motion direction
    __velocity=0.0        # Velocity for the motion direction
    __acceleration=0.0    # Acceleration in the direction of orientation

    def __init__(self, mass=1, kineticCOF=1, staticCOF=1):
        '''
        Constructor
        '''
        self.__mass=mass
        self.__kineticCOF=kineticCOF
        self.__staticCOF=staticCOF

    def getLocation(self):
        return(self.__location)
    
    def setLocation(self, location):
        self.__location = location
        
    def getOrientation(self):
        return(self.__orientation)
    
    def setOrientation(self, orientation):
        self.__orientation = orientation

    def getMass(self):
        return(self.__mass)
    
    def setMass(self, mass):
        self.__mass = mass
        
    def getStaticCOF(self):
        return(self.__staticCOF)
    
    def setStaticCOF(self, staticCOF):
        self.__staticCOF = staticCOF

    def getKineticCOF(self):
        return(self.__kineticCOF)
    
    def setKineticCOF(self, kineticCOF):
        self.__kineticCOF = kineticCOF

    def thrust(self, force, time):
        if self.__velocity==0.0 and force<=self.__staticCOF:
                self.__acceleration = 0
        else:
            if force>0:
                self.__acceleration = force/self.__mass - self.__kineticCOF
            else:
                self.__acceleration = force/self.__mass + self.__kineticCOF
        # TODO: Collision handling?
    
    def rotate(self, angle):
        self.__orientation = self.__orientation + angle
    
    