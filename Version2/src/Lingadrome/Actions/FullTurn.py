'''
Created on 2016/07/13

@author: rondelion
'''
import math

class FullTurn(object):
    '''
    classdocs
    '''
    __AngleAllowance = 0.01 * math.pi

    def __init__(self):
        '''
        Constructor
        '''
        self.turning = False
        self.originalOrientation = 0.0

    def action(self, input, states, parameters):
        steering = 0.2
        if not (input.has_key("orientation") and input["orientation"]!=None):
            states["locomotionType"] = ""
        else:
            if states.has_key("firstAfterSelection") and states["firstAfterSelection"]:
                self.originalOrientation = self.NormalizeRadian(input["orientation"])
                states["firstAfterSelection"] = False
            orientation = self.NormalizeRadian(input["orientation"])
            if parameters.has_key("turnDirection"):
                if parameters["turnDirection"] == "L":
                    steering = steering * -1.0
            states["steering"] = steering
            states["thrust"] = 0.0
            # print "FullTurn:", abs(orientation - self.originalOrientation)
            if abs(orientation - self.originalOrientation) < self.__AngleAllowance:
                if self.turning:
                    states["locomotionType"] = ""   # Finish turning
                    self.turning = False
            else:
                self.turning=True
        return
    
    def getName(self):
        return "Turn"

    @staticmethod
    def NormalizeRadian(rad):
        sin = math.sin(rad)
        cos = math.cos(rad)
        if rad > 0:
            if sin > 0:
                val = rad % math.pi
            else:
                val = rad % math.pi - math.pi
        elif rad < 0:
            if sin < 0:
                val = ((-1.0 * rad) % math.pi) * -1.0
            else:
                val = math.pi - ((-1.0 * rad) % math.pi)
        else:
            val = rad
        return val
