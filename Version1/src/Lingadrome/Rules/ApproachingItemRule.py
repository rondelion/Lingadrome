'''
Created on 2016/05/16

@author: rondelion
'''
import random
from Rule import Rule
import math

class ApproachingItemRule(Rule):
    '''
    Behavior of Approaching to an Item
    '''
    __score=25   # [0,100]
    __AngleAllowance=0.01 * math.pi
    __OffLimit=0.05

    def __init__(self):
        '''
        Constructor
        '''
        self.__phase = 1

    def condition(self, inputBuffer, stateBuffer):
        if inputBuffer.has_key("mostSalientItem") or inputBuffer.has_key("attendedItem"):
            return True
        else:
            return False
    
    def action(self, inputBuffer, stateBuffer):
        thrust=0.0
        steering=0.0
        values={}
        attendedItem = None
        if inputBuffer.has_key("attendedItem") and inputBuffer["attendedItem"]!=None:
            attendedItem = inputBuffer["attendedItem"]
            # print inputBuffer["name"], "attends", attendedItem
        else:
            mostSalient = inputBuffer["mostSalientItem"]
            if mostSalient != None and mostSalient.has_key("name"):
                attendedItem = mostSalient
        if attendedItem != None:
            values["attendedItemName"] = attendedItem["name"]
            if inputBuffer.has_key("orientation"):
                if attendedItem.has_key("direction") and attendedItem.has_key("distance"):
                    if inputBuffer.has_key("carryingDirection"):
                        carryingDirection = inputBuffer["carryingDirection"]
                    itemDirection = attendedItem["direction"]
                    orientation = inputBuffer["orientation"]
                    distance = attendedItem["distance"]
                    itemAbsoluteDirection = orientation + itemDirection
                    diff = ApproachingItemRule.NormalizeRadian(carryingDirection - itemAbsoluteDirection)
                    # print inputBuffer["name"], attendedItem["name"], carryingDirection, orientation, itemDirection
                    # if not in the carrying angle allowance
                    if self.__phase == 2:
                        diff2 = ApproachingItemRule.NormalizeRadian(orientation - carryingDirection)
                        # if not in the carrying angle allowance
                        if abs(diff2) > self.__AngleAllowance:
                            if inputBuffer["name"] == "BubbleRob#1":
                                print "orientation=", orientation, "carryingDirection=", carryingDirection, "diff2=", diff2
                            if diff2 < 0:  # orientation - carryingDirection
                                steering = -0.1
                            else:
                                steering = 0.1
                        else:
                            self.__phase = 3
                    elif self.__phase == 3:
                        diff2 = ApproachingItemRule.NormalizeRadian(orientation - carryingDirection)
                        thrust = 0.5
                        if inputBuffer["name"] == "BubbleRob#1":
                            print "carryingDirection=", carryingDirection, "itemAbsoluteDirection=", itemAbsoluteDirection, "diff=", diff
                        if diff2 > 0:  # carryingDirection - itemAbsoluteDirection
                            steering = 0.1
                        else:
                            steering = -0.1
                    elif abs(diff) > self.__AngleAllowance:
                        approachingAngleOffset = math.atan2(distance - self.__OffLimit, distance * diff)
                        approachingAngle = 0
                        if diff > 0:
                            approachingAngle = ApproachingItemRule.NormalizeRadian(itemAbsoluteDirection + approachingAngleOffset - 0.5 * math.pi)
                        else:
                            approachingAngle = ApproachingItemRule.NormalizeRadian(itemAbsoluteDirection + approachingAngleOffset + 0.5 * math.pi)
                        diff2 = ApproachingItemRule.NormalizeRadian(orientation - approachingAngle)
                        if inputBuffer["name"] == "BubbleRob#1":
                            print "diff=", diff, "orientation=", orientation, "approachingAngle=", approachingAngle, \
                            "itemAbsoluteDirection=", itemAbsoluteDirection, "diff2", diff2
                        # if not in the approaching angle allowance
                        if abs(diff2) > self.__AngleAllowance:
                            thrust = 0.0
                        else:
                            thrust = 0.5
                        steering = 0.1
                        if diff2 > 0:
                            steering = 0.1
                        elif diff2 < 0:
                            steering = -0.1
                    else:
                        self.__phase = 2
        values["steering"]=steering
        values["thrust"]=thrust
        # if inputBuffer["name"] == "BubbleRob#1":
        #    print inputBuffer["name"], "values", values
        return values
    
    def getName(self):
        return "ApproachingItem"
    
    def getScore(self):
        return self.__score

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
