'''
Created on 2015/10/20

@author: rondelion
'''
from Lingadrome.Rule import Rule

class FollowMostSalientRule(Rule):
    '''
    classdocs
    '''
    __score=10

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def condition(self, inputBuffer, stateBuffer):
        return True
    
    def action(self, inputBuffer, stateBuffer):
        thrust=0.5
        steering=0.0
        if inputBuffer.has_key("velocity") and inputBuffer["velocity"]>0.03:
            thrust=0.0
        if inputBuffer.has_key("mostSalient"):
            mostSalient=inputBuffer["mostSalient"]
            if mostSalient.has_key("orientation"):
                # print mostSalient["name"], mostSalient["orientation"], mostSalient["score"]
                if mostSalient["orientation"]<0:
                    steering=0.1
                else:
                    steering=-0.1
        else:
            thrust=0.0
            steering=0.5
        values={}
        values["steering"]=steering
        values["thrust"]=thrust
        return values
    
    def getName(self):
        return "FollowMostSalient"
    
    def getScore(self):
        return self.__score