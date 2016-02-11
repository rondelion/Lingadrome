'''
Created on 2016/01/18

@author: rondelion
'''
import datetime
from Rule import Rule

class BackOffRule2(Rule):
    '''
    classdocs
    '''
    __score=90
    __backOffDuration=500000 # micro-second
    __blockedDuration=30  # micro-second
    __thrustLimit = 0.1
    __velocityLimit = 0.001

    def __init__(self):
        '''
        Constructor
        '''
        self.__blocked = False
        self.__backOff = False
        self.__driveBackStartTime = 0
        self.__velocityHistory = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        self.__counter = 0
        self.__ready = False
    
    def condition(self, inputBuffer, stateBuffer):
        vsum = 0.0
        if inputBuffer.has_key("velocity"):
            self.__velocityHistory[self.__counter]=inputBuffer["velocity"]
            if self.__counter==19:
                self.__ready = True
            self.__counter = (self.__counter + 1) % 20
        if self.__ready:
            for v in self.__velocityHistory:
                vsum = vsum + v
        averageVelocity = vsum / 20.0
        # if it remains with thrust and without velocity then back off.
        if self.__ready and stateBuffer.has_key("thrust") and stateBuffer["thrust"]>self.__thrustLimit and \
           averageVelocity <self.__velocityLimit:
            if not self.__blocked:
                self.__blocked = True
                self.__blockedTime = datetime.datetime.now()
        else:
            self.__blocked = False
        if self.__blocked:
            if inputBuffer["name"]=="BubbleRob#0":
                print averageVelocity, stateBuffer["thrust"]
            blockedTime = datetime.datetime.now()-self.__blockedTime
            if blockedTime.microseconds > self.__blockedDuration:
                self.__driveBackStartTime = datetime.datetime.now()
                self.__backOff = True
                return True
            else:
                return False
        if self.__backOff:
            backOffTime = datetime.datetime.now()-self.__driveBackStartTime
            if backOffTime.microseconds < self.__backOffDuration:
                return True
            else:
                self.__backOff = False
                return False
        else:
            return False
    
    def action(self, inputBuffer, stateBuffer):
        thrust=0.0
        steering=0.0
        values={}
        if self.__backOff:
            # driving backwards while slightly turning:
            thrust=-1.0
            steering=-1.0
        values["steering"]=steering
        values["thrust"]=thrust
        return values
    
    def getName(self):
        return "BackOff2"
    
    def getScore(self):
        return self.__score