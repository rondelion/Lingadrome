'''
Created on 2016/07/11

@author: rondelion
'''
import random
import datetime

class LocomotionSelector(object):
    '''
    Selects types of locomotion
    '''
    __locomotionTypes = ["Stop", "GoStraight", "Turn", "FullTurn"] # , "Approach", "Carry"]
    __defaultDuration = 5 # in seconds

    def __init__(self):
        '''
        Constructor
        '''
        self.locomotionType = ""
        # Stop, GoAhead, Turn, FullTurn, Approach, Carry
        self.steering=0
        self.thrust=0
        self.carryingDirection=0
        self.salientItem=None
        self.selectTime = None

    def selectLocomotion(self, input, states):
        if states.has_key("locomotionType"):
            self.locomotionType = states["locomotionType"]
        else:
            self.locomoitonType = ""
        if self.selectTime != None:
            elapsed = datetime.datetime.now() - self.selectTime
            # print input["name"] + " selectLocomotion elapsed:", elapsed.seconds
            if elapsed.seconds > self.__defaultDuration:
                self.locomotionType = ""
        if self.locomotionType == "":
            self.locomotionType = random.choice(self.__locomotionTypes)
            self.selectTime = datetime.datetime.now()
            states["firstAfterSelection"]=True
            print input["name"], self.locomotionType + " selected!"
        states["locomotionType"] = self.locomotionType