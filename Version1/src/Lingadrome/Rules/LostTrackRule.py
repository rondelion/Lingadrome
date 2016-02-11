'''
Created on 2015/10/20

@author: rondelion
'''
from Rule import Rule

class LostTrackRule(Rule):
    '''
    classdocs
    '''
    __score=15

    def __init__(self):
        '''
        Constructor
        '''
        self.__turnDuration=1500
    
    def condition(self, inputBuffer, stateBuffer):
        if inputBuffer.has_key("mostSalient") and inputBuffer["mostSalient"]==None:
            return True
        else:
            return False
    
    def action(self, inputBuffer, stateBuffer):
        values={}
        values["steering"]=0.1
        return values
    
    def getName(self):
        return "LostTrack"
    
    def getScore(self):
        return self.__score