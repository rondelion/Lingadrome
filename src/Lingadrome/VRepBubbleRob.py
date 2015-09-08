'''
Created on 2015/09/08

@author: rondelion
'''

class VRepBubbleRob(object):
    '''
    classdocs
    '''
    __velocity=0.0        # m/s
    __angularVelocity=0.0 # radian/s
    __orientation=0.0     # π radian
    __thrust=0.0          # Degree of thrust forward
    __steeringOrientation=0.0 # [-1,+1]
    __emotion=0

    def __init__(self, params):
        '''
        Constructor
        '''
    
    def setSteeringOrientation(self, orientation):
        # L/R wheel speed difference
        self.__steeringOrientation = orientation
        
    def setThrust(self, thrust):
        # Average wheel speed
        self.__thrust = thrust

    def getVelocity(self):
        return self.__velocity
        # simxGetObjectVelocity

    def getAngularVelocity(self):
        return self.__angularVelocity
        # simxGetObjectVelocity

    def getOrientation(self):
        return self.__orientation
        # simxGetObjectOrientation
    
    def setEmotionalExpression(self, emotion):
        self.__emotion=emotion
    
    def detectNearestItem(self):
        pass
        # return the id, direction, distance & features of the nearest item
    
    def setAttentionDirection(self, orientation):
        pass
    
    def setAttentionWidth(self, width):
        pass
    
