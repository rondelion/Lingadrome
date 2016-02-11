'''
Created on 2015/10/20

@author: rondelion
'''
from Rule import Rule

class GoStraightRule(Rule):
    '''
    classdocs
    '''
    __score=5

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def condition(self, inputBuffer, stateBuffer):
        return True
    
    def action(self, inputBuffer, stateBuffer):
        thrust=1.0
        steering=0.0
        if inputBuffer.has_key("velocity") and inputBuffer["velocity"]>0.03:
            thrust=0.0
        values={}
        values["steering"]=steering
        values["thrust"]=thrust
        return values
    
    def getName(self):
        return "GoStraight"
    
    def getScore(self):
        return self.__score