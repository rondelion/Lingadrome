'''
Created on 2015/10/19

@author: rondelion
'''

from Rules.BackOffRule import BackOffRule
from Rules.GoStraightRule import GoStraightRule
from Rules.FollowMostSalientRule import FollowMostSalientRule
from Rules.LostTrackRule import LostTrackRule
from Rules.ConfrontingRule import ConfrontingRule
from Rules.SpontaneousPromenadeRule import SpontaneousPromenadeRule

class AgentMind(object):
    '''
    classdocs
    '''
    __thresholdSalience=0.0
    __driveBackStartTime=-99000
    __lostTrackTurnStartTime=-99000

    def __init__(self):
        '''
        Constructor
        '''
        self.__rules=[]
        self.__states={}
        self.__input={}
        self.__buffer={}
        self.__rules.append(BackOffRule())
        self.__rules.append(GoStraightRule())
        self.__rules.append(FollowMostSalientRule())
        self.__rules.append(LostTrackRule())
        self.__rules.append(ConfrontingRule())
        self.__rules.append(SpontaneousPromenadeRule())
        # print "Constructing Agent Mind:", len(self.__rules)
        self.__states["driveBackStartTime"]=AgentMind.__driveBackStartTime
        self.__states["__lostTrackTurnStartTime"]=AgentMind.__lostTrackTurnStartTime

    def setInput(self, key, value):
        self.__input[key]=value
        self.__input["mostSalient"]=self.__selectMostSalient()
        
    def __getInput(self, key):
        if self.__input.has_key(key):
            return self.__input[key]
        else:
            return None
    
    def applyRules(self):
        self.__buffer={}
        names=[]
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
            #if key=="thrust":
            #    print "thrust:", self.__buffer[key]
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

    def __selectMostSalient(self):
        maxScore=-1.0
        maxItem=None
        if self.__input.has_key("perceivedItems"):
            for item in self.__input["perceivedItems"]:
                if item.has_key("score"):
                    if item["score"]>maxScore:
                        maxItem=item
                        maxScore=item["score"]
        if maxScore>AgentMind.__thresholdSalience:
            return maxItem
        else:
            return None

