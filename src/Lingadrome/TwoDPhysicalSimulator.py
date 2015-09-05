'''
Created on 2015/09/05

@author: rondelion
'''

class TwoDPhysicalSimulator(object):
    '''
    classdocs
    '''
    __walls={}
    __objects={}

    def __init__(self, params):
        '''
        Constructor
        '''
        
    def addWall(self, handle, wall):
        self.__walls[handle]=wall
        
    def addObject(self, handle, twoDObject):
        self.__objects[handle]=twoDObject
    
    def getObject(self, handle):
        return self.__objects[handle]
    
    def elapse(self, time):
        # let time pass
        pass
    
    