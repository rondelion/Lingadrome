# -*- coding: utf-8 -*-
'''
Created on 2015/08/28

@author: rondelion
'''

class VRepObject(object):
    '''
    classdocs
    '''
    __location=(0.0,0.0)  # Object location (meter^2)
    __orientation=0.0     # π radian
    __thrust=0.0          # Degree of thrust forward
    __steeringOrientation=0.0 # [-1,+1]


    def getLocation(self):
        return(self.__location)
    
    def setLocation(self, location):
        self.__location = location
        
    def getOrientation(self):
        return(self.__orientation)
    
    def setOrientation(self, orientation):
        self.__orientation = orientation

    def getSteeringOrientation(self):
        return(self.__steeringOrientation)

    def setSteeringOrientation(self, orientation):
        # Actual orientation is determined by the physics engine used
        self.__steeringOrientation = orientation
        
    def getThrust(self):
        return(self.__thrust)

    def setThrust(self, thrust):
        # Actual orientation is determined by the physics engine used
        self.__thrust = thrust
        
    
    
    