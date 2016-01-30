'''
Created on 2016/01/30

@author: rondelion
'''
import random
from Rule import Rule

class ItemCarryingRule(Rule):
    '''
    Behavior of Item Carrying
    '''
    __enterCarryingModeDistance = 0.2
    __leaveCarryingModeDistance = 0.3
    __score=25   # [0,100]
    __distanceRange=1.0
    __orientationRange=0.1
    __directionRange=0.1
    __dampingCoefficient=0.997
    __emotionRewardCoefficient=1.0

    def __init__(self):
        '''
        Constructor
        '''
        self.__itemCarrying=False
        self.__carryingDirection=0.0    # radian
    
    def condition(self, inputBuffer, stateBuffer):
        if inputBuffer.has_key("mostSalient"):
            mostSalient=inputBuffer["mostSalient"]
            if mostSalient!=None:
                if not mostSalient.has_key("orientation"):  # Item
                    if mostSalient.has_key("distance"):
                        msdst=mostSalient["distance"]
                        if msdst < ItemCarryingRule.__enterCarryingModeDistance and not self.__itemCarrying:
                            self.__itemCarrying=True
                            self.__carryingDirection = random.random()*2.0 # radian
                            print inputBuffer["name"], ": Entering Item Carrying Mode for direction: ", self.__carryingDirection
                            return True
                        if msdst > ItemCarryingRule.__leaveCarryingModeDistance and self.__itemCarrying:
                            print inputBuffer["name"], ": Leaving Item Carrying Mode."
                            self.__itemCarrying=False
                            return False
        return self.__itemCarrying
    
    def action(self, inputBuffer, stateBuffer):
        values={}
        return values
    
    def getName(self):
        return "ItemCarrying"
    
    def getScore(self):
        return self.__score