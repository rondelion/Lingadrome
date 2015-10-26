'''
Created on 2015/10/20

@author: rondelion
'''
import math

class ConfrontingRule(object):
    '''
    Detecting the most salient Agent facing each other
    '''
    __score=20   # [0,100]
    __distanceRange=1.0
    __orientationRange=0.1
    __directionRange=0.1

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def condition(self, inputBuffer, stateBuffer):
        if inputBuffer.has_key("orientation"):
            if inputBuffer.has_key("mostSalient"):
                mostSalient=inputBuffer["mostSalient"]
                if mostSalient!=None and mostSalient.has_key("direction") and mostSalient.has_key("distance"):
                    msdir=mostSalient["direction"]
                    msdst=mostSalient["distance"]
                    msori=mostSalient["orientation"]
                    revmsori=0.0
                    if msori<0.0:
                        revmsori=math.pi-msori
                    else:
                        revmsori=msori-math.pi
                    #if inputBuffer["name"]=="BubbleRob#1":
                    #    print msdir
                    if math.fabs(msdir)<ConfrontingRule.__directionRange:
                        if math.fabs(inputBuffer["orientation"]-revmsori)<ConfrontingRule.__orientationRange:
                            if msdst<ConfrontingRule.__distanceRange:
                                return True
        return False
    
    def action(self, inputBuffer, stateBuffer):
        if inputBuffer.has_key("mostSalient"):
            mostSalient=inputBuffer["mostSalient"]
            print "Confronting to ", mostSalient["name"]
        return {}   # Empty return buffer dictionary
    
    def getName(self):
        return "Confronting"
    
    def getScore(self):
        return self.__score