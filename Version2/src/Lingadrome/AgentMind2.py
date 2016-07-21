'''
Created on 2016/07/11

@author: rondelion
'''

from LocomotionSelector import LocomotionSelector
from Actions.Locomotion import Locomotion

class AgentMind2(object):
    '''
    classdocs
    '''
    __thresholdSalience=0.0
    __driveBackStartTime=-99000
    __lostTrackTurnStartTime=-99000

    def __init__(self, type):
        '''
        Constructor
        '''
        if type!="User" and type!="Learner":
            raise TypeError("AgentMind neither User nor Learner!")
        self.__type = type
        self.__rules=[]
        self.__states={}
        self.__input={}
        self.__actionParameters={}
        self.__buffer={}
        self.locomotionSelector = LocomotionSelector()
        self.locomotion = Locomotion()
        self.__states["driveBackStartTime"]=AgentMind2.__driveBackStartTime
        self.__states["__lostTrackTurnStartTime"]=AgentMind2.__lostTrackTurnStartTime

    def setInput(self, key, value):
        self.__input[key]=value

    def perceive(self):
        pass
        # for perception in self.__perceptions:
        #   perception.perceive(self.__input, self.__states)

    def selectAction(self):
        self.locomotionSelector.selectLocomotion(self.__input, self.__states)

    def action(self):
        self.locomotion.action(self.__input, self.__states, self.__actionParameters)
        # print self.__input["name"] + ":",  self.__states

    def getOutput(self, key):
        if self.__states.has_key(key):
            return self.__states[key]
        else:
            return None

    def selectMostSalient(self, type):
        maxScore=-1.0
        maxItem=None
        if self.__input.has_key("perceivedItems"):
            for item in self.__input["perceivedItems"]:
                if item.has_key("score"):
                    if (type=="A" and item.has_key("orientation")) or (type=="I" and not item.has_key("orientation")):
                        if item["score"]>maxScore:
                            maxItem=item
                            maxScore=item["score"]
        if maxScore>AgentMind2.__thresholdSalience:
            return maxItem
        else:
            return None

    def getAttendedItem(self, name):
        if self.__input.has_key("perceivedItems"):
            for item in self.__input["perceivedItems"]:
                if item["name"] == name:
                    return item
        return None

