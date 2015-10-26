# -*- coding: utf-8 -*-
'''
Created on 2015/09/08

@author: rondelion
'''
import sys
import math
from AgentMind import AgentMind
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

class VRepAgent(object):
    '''
    classdocs
    '''
    __DistanceSalienceAttenuationCoefficient=-1.0

    def __init__(self, name, clientID, sensorHandle, bodyHandle):
        '''
        Constructor
        '''
        self.__velocity=0.0        # m/s
        self.__angularVelocity=0.0 # radian/s
        self.__orientation=None    # π radian
        self.__steering=0.0        # Steering value [-1,1]
        self.__thrust=1.0          # Accelerator value [-1,1]
        self.__emotion=0
        self.__position=None
        self.__initLoop=True
        self.__perceivedItems={}
        self.__mind=AgentMind()
        self.__name=name
        self.__clientID=clientID          # Client ID of the V-Rep agent
        self.__sensorHandle=sensorHandle  # Proximity sensor handle of the V-Rep agent
        self.__bodyHandle=bodyHandle      # BubbleRob body handle
        self.__driveBackStartTime=-99000
        self.__firstOrientation=None
        self.__cnt=0
        self.__mind.setInput("name", name)
   
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
            self.__orientation=orientation[2]
        else:
            self.__orientation = None
            # print >> sys.stderr, "Error in VRepBubbleRob.getOrientation()"
        self.__mind.setInput("orientation", self.__orientation)
        returnCode, position = vrep.simxGetObjectPosition(self.__clientID, self.__bodyHandle, -1, operationMode)
        if returnCode==vrep.simx_return_ok:
            self.__position=[0.0,0.0]
            self.__position[0]=position[0]  #X
            self.__position[1]=position[1]  #Y
        else:
            self.__position=None
            # print >> sys.stderr, "Error in VRepBubbleRob.getPosition()"
        returnCode, linearVelocity, angularVelocity = vrep.simxGetObjectVelocity(self.__clientID, self.__bodyHandle, operationMode)
        if returnCode==vrep.simx_return_ok:
            try:
                self.__velocity=linearVelocity[0]*math.cos(self.__orientation)+linearVelocity[1]*math.sin(self.__orientation)
                self.__mind.setInput("velocity", self.__velocity)
            except TypeError:
                pass
                # if self.__name=="BubbleRob#1":
                #    print self.__velocity, linearVelocity[0], math.cos(self.__orientation), linearVelocity[1], math.sin(self.__orientation)
        else:
            self.__velocity=None
            # print >> sys.stderr, "Error in VRepBubbleRob.getPosition()"
        returnCode, sensorTrigger, dp, doh, dsnv = vrep.simxReadProximitySensor(self.__clientID, self.__sensorHandle, operationMode)
        if returnCode==vrep.simx_return_ok:
            # We succeeded at reading the proximity sensor
            self.__mind.setInput("lastProximitySensorTime", vrep.simxGetLastCmdTime(self.__clientID))
            self.__mind.setInput("sensorTrigger", sensorTrigger)
        self.__mind.applyRules()
        self.__mind.setStates()
        if self.__mind.getOutput("steering")!=None:
            self.setSteering(self.__mind.getOutput("steering"))
        if self.__mind.getOutput("thrust")!=None:
            self.setThrust(self.__mind.getOutput("thrust"))
        getSignalReturnCode, dMessage = vrep.simxGetStringSignal(self.__clientID, "Debug", vrep.simx_opmode_streaming)
        if dMessage!="":
            print("Debug:"+dMessage)
        self.__cnt=self.__cnt+1
            
    def setSteering(self, steering):
        # Steering value [-1,1]
        self.__steering = steering
        #if self.getName()=="BubbleRob#1":
        #    print self.getName(), steering
        vrep.simxSetFloatSignal(self.__clientID, self.__name+":Steering", self.__steering, vrep.simx_opmode_oneshot)
        # print self.__clientID, self.__name+":Steering", self.__steering
        
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
        self.__visualSalience()
        self.__mind.setInput("perceivedItems", self.__perceivedItems)

    def __visualSalience(self):
        # give the score to perceived items
        for item in self.__perceivedItems:
            score=0.0
            if item.has_key("direction") and item.has_key("distance"):
                direction=item["direction"]
                if -0.5*math.pi<direction and direction<0.5*math.pi:
                    # FOV: [-90,90] degrees
                    score=math.cos(direction)*math.exp(VRepAgent.__DistanceSalienceAttenuationCoefficient*item["distance"])
            item["score"]=score

