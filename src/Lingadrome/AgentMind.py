'''
Created on 2015/10/19

@author: rondelion
'''

from BackOffRule import BackOffRule
from GoStraightRule import GoStraightRule
from FollowMostSalientRule import FollowMostSalientRule
from Finder.Finder_items import item

class AgentMind(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__rules=[]
        self.__states={}
        self.__input={}
        self.__buffer={}
        self.__driveBackStartTime=-99000
        self.__rules.append(BackOffRule())
        self.__rules.append(GoStraightRule())
        self.__rules.append(FollowMostSalientRule())
        # print "Constructing Agent Mind:", len(self.__rules)
        self.__states["driveBackStartTime"]=self.__driveBackStartTime

    def setInput(self, key, value):
        self.__input[key]=value
        maxSalient=self.__selectMostSalient()
        if maxSalient!=None:
            self.__input["mostSalient"]=maxSalient
        
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
        return maxItem

