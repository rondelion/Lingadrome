'''
Created on 2016/02/11

@author: rondelion
'''
from scipy import zeros
from pybrain.rl.environments import Environment

class LocomotionEnvironment(Environment):
    '''
    classdocs
    '''
    def getSensors(self):
        obs = zeros(4)
        return obs

    def performAction(self, action):
        pass