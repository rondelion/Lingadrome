'''
Created on 2016/07/11

@author: rondelion
'''

from Perception.Perceive import Perceive
from LocomotionSelector import LocomotionSelector
from Actions.Locomotion import Locomotion
from Reward.Reward import Reward

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
        self.states={"reward":0, "sanction":0}
        self.input={}
        self.actionParameters={}
        self.__buffer={}
        self.locomotionSelector = LocomotionSelector()
        self.locomotion = Locomotion()
        self.perception = Perceive()
        self.reward = Reward()

    def setInput(self, key, value):
        self.input[key]=value

    def perceive(self):
        self.perception.perceive(self.input, self.states)
        # for perception in self.__perceptions:
        #   perception.perceive(self.input, self.states)

    def setReward(self):
        self.reward.reward(self.input, self.states)

    def selectAction(self):
        self.locomotionSelector.selectLocomotion(self.input, self.states, self.actionParameters)

    def action(self):
        self.locomotion.action(self.input, self.states, self.actionParameters)
        #if self.input["name"]=="BubbleRob#0":
        #    print self.input["name"] + ":",  self.states, self.actionParameters

    def getOutput(self, key):
        if self.states.has_key(key):
            return self.states[key]
        else:
            return None

    def selectMostSalient(self, type):
        maxScore=-1.0
        maxItem=None
        if self.input.has_key("perceivedItems"):
            for item in self.input["perceivedItems"]:
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
        if self.input.has_key("perceivedItems"):
            for item in self.input["perceivedItems"]:
                if item["name"] == name:
                    return item
        return None
