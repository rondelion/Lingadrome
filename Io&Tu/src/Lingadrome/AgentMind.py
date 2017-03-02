'''
Created on 2016/11/06

@author: rondelion
'''


class AgentMind(object):
    '''
    classdocs
    '''

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
        self.reward = 0
        self.count = 0

    def loop(self):
        self.selectAction()
        self.count = self.count + 1

    def setInput(self, key, value):
        self.input[key]=value

    def setReward(self, reward):
        self.reward = reward

    def selectAction(self):
        pass

    def getOutput(self, key):
        if self.states.has_key(key):
            return self.states[key]
        else:
            return None
