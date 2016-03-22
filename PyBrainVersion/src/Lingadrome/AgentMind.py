'''
Created on 2015/10/19

@author: rondelion
'''
from pybrain.rl.agents import LearningAgent

from BackOffRule2 import BackOffRule2
from Locomotion.LocomotionPrimitives import LocomotionPrimitives

class AgentMind(LearningAgent):
    '''
    classdocs
    '''
    __thresholdSalience=0.0
    __driveBackStartTime=-99000
    __lostTrackTurnStartTime=-99000

    def __init__(self, module, learner = None):
        '''
        Constructor
        '''
        LearningAgent.__init__(self, module, learner)
        self.__rules=[]
        self.__states={}
        self.__input={}
        self.__buffer={}
        # self.__rules.append(BackOffRule())
        self.__rules.append(BackOffRule2())
        self.__rules.append(LocomotionPrimitives())
        self.__states["driveBackStartTime"]=AgentMind.__driveBackStartTime
        self.__states["__lostTrackTurnStartTime"]=AgentMind.__lostTrackTurnStartTime

    def setInput(self, key, value):
        self.__input[key]=value
        
    def __getInput(self, key):
        if self.__input.has_key(key):
            return self.__input[key]
        else:
            return None
    
    def applyRules(self):
        self.__buffer={}
        names=[]
        self.__setMostSalient()
        self.__input["action"]=int(self.getAction())
        for rule in self.__rules:
            if not rule.getName() in names: # Do not remove this code
                names.append(rule.getName())
                if rule.condition(self.__input, self.__states):
                    values = rule.action(self.__input, self.__states)
                    score = rule.getScore()
                    for key in values:
                        if not self.__buffer.has_key(key):
                            self.__buffer[key]=[]
                        self.__buffer[key].append([values[key], score])
    
    def setStates(self):
        for key in self.__buffer.keys():
            maxScore = -1
            value = None
            for item in self.__buffer[key]:
                if maxScore < item[1]:
                    value = item[0]
                    maxScore = item[1]
            self.__states[key]=value
        
    def getOutput(self, key):
        if self.__states.has_key(key):
            return self.__states[key]
        else:
            return None

    def __setMostSalient(self):
        if self.__input.has_key("perceivedItems"):
            items = self.__input["perceivedItems"]
            self.__input["mostSalientItem"]=self.__selectMostSalient(items)
        # if self.__input.has_key("perceivedAgents"):
        #    agents = self.__input["perceivedAgents"]
        #    self.__input["mostSalientAgent"]=self.__selectMostSalient(agents)
        
    def __selectMostSalient(self, objects):
        maxScore=-1.0
        maxItem=None
        for item in objects:
            if item.has_key("score"):
                if item["score"]>maxScore:
                    maxItem=item
                    maxScore=item["score"]
        if maxScore>AgentMind.__thresholdSalience:
            return maxItem
        else:
            return None

    def getMostSalientAgent(self):
        if self.__input.has_key("mostSalientAgent"):
            return self.__input["mostSalientAgent"]
        else:
            return None

    def getMostSalientItem(self):
        if self.__input.has_key("mostSalientItem"):
            return self.__input["mostSalientItem"]
        else:
            return None
