'''
Created on 2016/02/08

@author: rondelion
'''
from pybrain.rl.environments.task import Task

class LocomotionTask(Task):
    '''
    classdocs
    '''
    def getReward(self):
        return 1.0