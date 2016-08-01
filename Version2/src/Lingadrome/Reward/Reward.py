'''
Created on 2016/07/31

@author: rondelion
'''
from ConfrontingReward import ConfrontingReward

class Reward(object):
    '''
    classdocs
    '''
    __dampingCoefficient=0.997

    def __init__(self):
        '''
        Constructor
        '''
        self.confrontingReward = ConfrontingReward()

    def reward(self, input, states):
        self.confrontingReward.reward(input, states)
        states["reward"] = states["reward"] * self.__dampingCoefficient
