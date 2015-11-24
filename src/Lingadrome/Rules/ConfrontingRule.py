'''
Created on 2015/10/20

@author: rondelion
'''
import math
from Rule import Rule

class ConfrontingRule(Rule):
    '''
    Detecting the most salient Agent facing each other
    '''
    __score=20   # [0,100]
    __distanceRange=1.0
    __orientationRange=0.1
    __directionRange=0.1
    __dampingCoefficient=0.8

    def __init__(self):
        '''
        Constructor
        '''
        self.__current=False
        self.__previous=False
        self.__reward=0.0
    
    def condition(self, inputBuffer, stateBuffer):
        self.__previous=self.__current
        self.__current=False
        if inputBuffer.has_key("orientation"):
            if inputBuffer.has_key("mostSalient"):
                mostSalient=inputBuffer["mostSalient"]
                if mostSalient!=None and mostSalient.has_key("direction") and mostSalient.has_key("distance"):
                    msdir=mostSalient["direction"]
                    msdst=mostSalient["distance"]
                    msori=mostSalient["orientation"]
                    revmsori=0.0
                    if msori<0.0:
                        revmsori=math.pi+msori
                    else:
                        revmsori=msori-math.pi
                    # if inputBuffer["name"]=="BubbleRob#0":
                    #    print inputBuffer["orientation"], revmsori, msori
                    if math.fabs(msdir)<ConfrontingRule.__directionRange:
                        if math.fabs(inputBuffer["orientation"]-revmsori)<ConfrontingRule.__orientationRange:
                            if msdst<ConfrontingRule.__distanceRange:
                                self.__current=True
        return self.__current
    
    def action(self, inputBuffer, stateBuffer):
        values={}
        if self.__current and not self.__previous:
            self.__reward=1.0
        else:
            self.__reward=self.__reward * self.__dampingCoefficient
        values["reward"]=self.__reward
        if inputBuffer.has_key("mostSalient"):
            mostSalient=inputBuffer["mostSalient"]
            # print "Confronting to ", mostSalient["name"]
        return values
    
    def getName(self):
        return "Confronting"
    
    def getScore(self):
        return self.__score