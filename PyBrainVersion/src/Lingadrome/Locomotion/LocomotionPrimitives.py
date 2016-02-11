'''
Created on 2016/02/07

@author: rondelion
'''
import datetime
import random
from Rule import Rule

class LocomotionPrimitives(Rule):
    '''
    classdocs
    '''
    __score=90
    __Interval=100000 # 0.1sec. in micro-second

    def __init__(self):
        '''
        Constructor
        '''
        self.__prevTime=None
        self.__values={}
    
    def condition(self, inputBuffer, stateBuffer):
        return True

    def chooseFrom(self, alt):
        return int(random.random()*alt)
        
    def selectAction(self):
        values={}
        thrust=0.0
        steering=0.0
        action = self.chooseFrom(5)
        if action==0:   # go straight
            thrust=1.0
        elif action==1: # steer to right
            thrust=0.5
            steering=0.5
        elif action==2: # steer to left
            thrust=0.5
            steering=-0.5
        elif action==3: # back off to right
            thrust=-0.5
            steering=0.5
        elif action==4: # back off to left
            thrust=-0.5
            steering=-0.5
        values["steering"]=steering
        values["thrust"]=thrust
        return values
        
    def action(self, inputBuffer, stateBuffer):
        # set a new action for each interval
        values={}
        current = datetime.datetime.now()
        if self.__prevTime!=None:
            elapsed = current - self.__prevTime
            if elapsed.microseconds > self.__Interval:
                values=self.selectAction()
                self.__prevTime = current
        else:
            values=self.selectAction()
            self.__prevTime = current
        print "LocomotionPrimitives in action"
        return values

    def getName(self):
        return "LocomotionPrimitives"
    
    def getScore(self):
        return self.__score