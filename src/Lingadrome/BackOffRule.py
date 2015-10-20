'''
Created on 2015/10/20

@author: rondelion
'''
from Lingadrome.Rule import Rule

class BackOffRule(Rule):
    '''
    classdocs
    '''
    __score=100

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def condition(self, inputBuffer, stateBuffer):
        return True
    
    def action(self, inputBuffer, stateBuffer):
        thrust=0.0
        steering=0.0
        values={}
        if inputBuffer.has_key("lastProximitySensorTime") and stateBuffer.has_key("driveBackStartTime"):
            lastProximitySensorTime=inputBuffer["lastProximitySensorTime"]
            if lastProximitySensorTime-stateBuffer["driveBackStartTime"]<3000:
                # driving backwards while slightly turning:
                thrust=-1.0
                steering=-1.0
            else:
            # going forward:
                thrust=1.0
                steering=0.0
                if inputBuffer.has_key("sensorTrigger") and inputBuffer["sensorTrigger"]:
                    # We detected something, and start the backward mode
                    values["driveBackStartTime"]=lastProximitySensorTime
            values["steering"]=steering
            values["thrust"]=thrust
        return values
    
    def getName(self):
        return "BackOff"
    
    def getScore(self):
        return self.__score