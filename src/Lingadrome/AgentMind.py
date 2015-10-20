'''
Created on 2015/10/19

@author: rondelion
'''

from BackOffRule import BackOffRule

class AgentMind(object):
    '''
    classdocs
    '''
    __input={}
    __buffer={}
    __states={}
    __rules=[]
    __driveBackStartTime=-99000

    def __init__(self):
        '''
        Constructor
        '''
        self.__rules.append(BackOffRule())
        self.__states["driveBackStartTime"]=self.__driveBackStartTime

    def setInput(self, key, value):
        self.__input[key]=value
        
    def __getInput(self, key):
        if self.__input.has_key(key):
            return self.__input[key]
        else:
            return None
    
    def applyRules(self):
        self.__buffer={}
        for rule in self.__rules:
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

