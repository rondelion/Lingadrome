'''
Created on 2015/12/15

@author: rondelion
'''
import datetime
import math
from Lingadrome.Rules.Rule import Rule

class SpontaneousPromenadeRule(Rule):
    '''
    Rule to cause spontaneous promenade
    '''
    __score=30
    __velocityThreshold=0.0001
    __urgeThreshold=40
    __actionPotentialThreshold=20.0
    __dampingCoefficient=0.997
    __turnDuration=500000       # in microseconds

    def __init__(self):
        '''
        Constructor
        '''
        self.__urge=0
        self.__actionPotential=0.0
        self.__fireTime=None
    
    def condition(self, inputBuffer, stateBuffer):
        # The urge increases while staying still
        if inputBuffer.has_key("velocity") and math.fabs(inputBuffer["velocity"])<self.__velocityThreshold:
            self.__urge=self.__urge + 1
        else:
            self.__urge=0
        if self.__urge > self.__urgeThreshold:
            # action potential overshoots if the urge exceeds the threshold
            if self.__actionPotential <  self.__actionPotentialThreshold:
                self.__actionPotential=100.0
                self.__fireTime = datetime.datetime.now()
        self.__actionPotential = self.__actionPotential * self.__dampingCoefficient
        # return True while action potential overshoots
        if self.__actionPotential >  self.__actionPotentialThreshold:
            return True
        else:
            return False
    
    def action(self, inputBuffer, stateBuffer):
        thrust=0.0
        steering=0.0
        values={}
        elapsed = datetime.datetime.now()-self.__fireTime
        if elapsed.microseconds<self.__turnDuration:
            # driving backwards while slightly turning after the overshoot
            thrust=-0.5
            steering=-1.0
        else:   # go straight
            thrust=1.0
            steering=0.0
            if inputBuffer.has_key("velocity") and inputBuffer["velocity"]>0.03:
                thrust=0.0
        values["steering"]=steering
        values["thrust"]=thrust
        return(values)

    def getName(self):
        return "SpontaneousPromenade"
    
    def getScore(self):
        return self.__score