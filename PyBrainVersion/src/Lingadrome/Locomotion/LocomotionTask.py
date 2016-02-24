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
    SalientItemDistanceNumber = 3   # 0:Contact, 1:Near, 2:Far
    SalientItemDirectionNumber = 5  # 0:Ahead, 1:RightForward, 2:LeftForward, 3:RightBackward, 4:LeftBackward
    HeadingDirectionNumber = 5  # 0:Ahead, 1:RightForward, 2:LeftForward, 3:RightBackward, 4:LeftBackward
    BlockedStatusNumber = 2     # 0:Free, 1:Blocked
    
    def __init__(self, environment):
        '''
        Constructor
        '''
        Task.__init__(self, environment)
        self.__observationArray = [0,0,0,0] # SalientItemDistance, SalientItemDirection, HeadingDirection, BlockedStatus

    def getReward(self):
        return 1.0

    def getObservation(self):
        obs = array([((self.__observationArray[0]*self.SalientItemDirectionNumber + \
                       self.__observationArray[1])*self.HeadingDirectionNumber + \
                       self.__observationArray[2])*self.BlockedStatusNumber + \
                       self.__observationArray[3]])
        return obs
