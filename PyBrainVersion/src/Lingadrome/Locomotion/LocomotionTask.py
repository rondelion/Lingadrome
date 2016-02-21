'''
Created on 2016/02/08

@author: rondelion
'''
from scipy import array
from pybrain.rl.environments.task import Task

class LocomotionTask(Task):
    '''
    classdocs
    '''
    def getReward(self):
        return 1.0

    def getObservation(self):
        obs = array([0])
        return obs
