# -*- coding: utf-8 -*-
'''
Created on 2015/09/08

@author: rondelion
'''
import sys
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

class VRepBubbleRob(object):
    '''
    classdocs
    '''
    __name=""
    __clientID=0          # Client ID of the V-Rep agent
    __sensorHandle=0      # Proximity sensor handle of the V-Rep agent
    __bodyHandle=0        # BubbleRob body handle
    __velocity=0.0        # m/s
    __angularVelocity=0.0 # radian/s
    __orientation=None    # π radian
    __emotion=0
    __steering=0.0    # Steering value [-1,1]
    __thrust=1.0      # Degree of thrust forward [-1,1]
    __driveBackStartTime=-99000
    __position=None
    __initLoop=True
    __perceivedItems={}

    def __init__(self, name, clientID, sensorHandle, bodyHandle):
        '''
        Constructor
        '''
        self.__name=name
        self.__clientID=clientID
        self.__sensorHandle=sensorHandle
        self.__bodyHandle=bodyHandle
        self.__driveBackStartTime=-99000
        self.__steering=0.0         # Steering value [-1,1]
        self.__thrust=1.0     # Accelerator value [-1,1]
   
    def getClientID(self):
        return self.__clientID

    def getName(self):
        return self.__name

    def loop(self):
        operationMode=vrep.simx_opmode_streaming
        if self.__initLoop:
            self.__initLoop=False
        else:
            operationMode=vrep.simx_opmode_buffer
        returnCode, orientation = vrep.simxGetObjectOrientation(self.__clientID, self.__bodyHandle, -1, operationMode)
        if returnCode==vrep.simx_return_ok:
            self.__orientation=orientation[2]  #Z
        else:
            self.__orientation = None
            print >> sys.stderr, "Error in VRepBubbleRob.getOrientation()"
        returnCode, position = vrep.simxGetObjectPosition(self.__clientID, self.__bodyHandle, -1, operationMode)
        if returnCode==vrep.simx_return_ok:
            self.__position=[0.0,0.0]
            self.__position[0]=position[0]  #X
            self.__position[1]=position[1]  #Y
        else:
            print >> sys.stderr, "Error in VRepBubbleRob.getPosition()"
            self.__position=None
        returnCode, sensorTrigger, dp, doh, dsnv = vrep.simxReadProximitySensor(self.__clientID, self.__sensorHandle, operationMode)
        if returnCode==vrep.simx_return_ok:
            # We succeeded at reading the proximity sensor
            simulationTime=vrep.simxGetLastCmdTime(self.__clientID)
            thrust=0.0
            steering=0.0
            if simulationTime-self.__driveBackStartTime<3000:
                # driving backwards while slightly turning:
                thrust=-1.0
                steering=-1.0
            else:
                # going forward:
                thrust=1.0
                steering=0.0
                if sensorTrigger:
                    self.__driveBackStartTime=simulationTime # We detected something, and start the backward mode
            self.setSteering(steering)
            self.setThrust(thrust)
        getSignalReturnCode, dMessage = vrep.simxGetStringSignal(self.__clientID, "Debug", vrep.simx_opmode_streaming)
        if dMessage!="":
            print("Debug:"+dMessage)
    
    def setSteering(self, steering):
        # Steering value [-1,1]
        self.__steering = steering
        vrep.simxSetFloatSignal(self.__clientID, self.__name+":Steering", self.__steering, vrep.simx_opmode_oneshot)
        
    def setThrust(self, thrust):
        # Average wheel speed
        self.__thrust = thrust
        vrep.simxSetFloatSignal(self.__clientID, self.__name+":Acceleration", self.__thrust, vrep.simx_opmode_oneshot)

    def getPosition(self):
        return self.__position

    def getOrientation(self):
        return self.__orientation
    
    def getVelocity(self):
        return self.__velocity
        # simxGetObjectVelocity

    def getAngularVelocity(self):
        return self.__angularVelocity
        # simxGetObjectVelocity

    def setEmotionalExpression(self, emotion):
        self.__emotion=emotion
    
    def detectNearestItem(self):
        pass
        # return the id, direction, distance & features of the nearest item
    
    def setAttentionDirection(self, orientation):
        pass
    
    def setAttentionWidth(self, width):
        pass
    
    def setPerceivedItems(self, items):
        # set a list of perceived items
        self.__perceivedItems=items
