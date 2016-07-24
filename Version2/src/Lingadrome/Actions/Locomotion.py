'''
Created on 2016/07/13

@author: rondelion
'''
import random
from Stop import Stop
from GoStraight import GoStraight
from Turn import Turn
from FullTurn import FullTurn

class Locomotion(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.Stop = Stop()
        self.goStraight = GoStraight()
        self.Turn = Turn()
        self.FullTurn = FullTurn()

    def action(self, input, states, parameters):
        if states["locomotionType"] == "Stop":
            self.Stop.action(input, states, parameters)
        elif states["locomotionType"] == "GoStraight":
            self.goStraight.action(input, states, parameters)
        elif states["locomotionType"] == "Turn":
            self.Turn.action(input, states, parameters)
        elif states["locomotionType"] == "FullTurn":
            if input.has_key("orientation") and input["orientation"]!=None:
                self.FullTurn.action(input, states, parameters)
        elif states["locomotionType"] == "Approach":
            pass
        elif states["locomotionType"] == "Carry":
            pass
        # print "Locomotion.action.states:", states
