# -*- coding: utf-8 -*-
'''
Created on 2015/08/28

@author: rondelion
'''
from VRepObject import VRepObject
try:
    import vrep
except:
    print ('VRepBubbleRob--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')
    exit(-1)

class VRepItem(VRepObject):
    '''
    classdocs
    '''


    def __init__(self, name, clientID, handle):
        '''
        Constructor
        '''
        self.__name=name
        self.__clientID=clientID    # Client ID of the Dummy object
        self.__bodyHandle=handle        # VRep object handle
        self.__orientation=None    # π radian
        self.__position=None
        self.__initLoop=True
        self.__initPosition=None
        self.__cnt=0
    
    def getName(self):
        return self.__name

    def getType(self):
        return "Item"

    def loop(self):
        operationMode=vrep.simx_opmode_streaming
        if self.__initLoop:
            self.__initLoop=False
        else:
            operationMode=vrep.simx_opmode_buffer
        returnCode, position = vrep.simxGetObjectPosition(self.__clientID, self.__bodyHandle, -1, operationMode)
        if returnCode==vrep.simx_return_ok:
            self.__position=[0.0,0.0]
            self.__position[0]=position[0]  #X
            self.__position[1]=position[1]  #Y
            if self.__initPosition==None:
                self.__initPosition=self.__position
        else:
            self.__position=None
        self.__cnt=self.__cnt+1
    
    def getPosition(self):
        return self.__position

    def getInitPosition(self):
        return self.__initPosition
    
    def returnToInitPosition(self):
        vrep.simxSetObjectPosition(self.__clientID, self.__bodyHandle, -1, self.__initPosition, vrep.simx_opmode_oneshot)