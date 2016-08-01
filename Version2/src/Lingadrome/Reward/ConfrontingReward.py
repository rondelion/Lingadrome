'''
Created on 2016/07/29

@author: rondelion
'''
import math

class ConfrontingReward(object):
    '''
    classdocs
    '''
    __dampingCoefficient=0.997

    def __init__(self):
        '''
        Constructor
        '''
        self.__current = False
        self.__previous = False

    def reward(self, input, states):
        if input.has_key("MSAisInCenterFOV") and input.has_key("MSAisConfronting") \
                and input["MSAisInCenterFOV"] and input["MSAisConfronting"]:
            self.__current = True
        else:
            self.__current = False
        if self.__current and not self.__previous:
            states["reward"] = 1.0
