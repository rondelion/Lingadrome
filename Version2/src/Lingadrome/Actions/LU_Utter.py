'''
Created on 2016/08/11

@author: rondelion
'''
import datetime
import random

class LU_Utter(object):
    '''
    classdocs
    '''
    __name = {"BubbleRob#0": "Mario", "BubbleRob#0": "Luca"}
    __defaultDuration = 1 # in seconds
    __suppressDuration = 5 # in seconds
    __minimumSalience=0.1
    __itemAgentDistance2Approach=0.5

    def __init__(self):
        '''
        Constructor
        '''
        self.startTime = None
        self.endTime = None

    def action(self, input, states, parameters):
        potentialUtterance = []
        if input.has_key("MSAisInCenterFOV") and input["MSAisInCenterFOV"]:
            if input.has_key("MSAisConfronting") and not input["MSAisConfronting"]:
                potentialUtterance.append(LU_Utter.__name[input["name"]] + "!")
                potentialUtterance.append(LU_Utter.__name[input["name"]] + ", reguarda hic!")
            if input.has_key("MSAisInConfrontingDistance") and not input["MSAisInConfrontingDistance"]:
                potentialUtterance.append(LU_Utter.__name[input["name"]] + ", veni hic!")
            potentialUtterance.append(LU_Utter.__name[input["name"]] + ", resta!")
            potentialUtterance.append(LU_Utter.__name[input["name"]] + ", gira!")
            msa = input["mostSalientAgent"]
            self.itemAction(input, msa["distance"], potentialUtterance)
        if len(potentialUtterance)>0:
            if self.endTime != None:
                suppressed = datetime.datetime.now() - self.endTime
            if self.startTime == None:
               if self.endTime == None or suppressed.seconds > self.__suppressDuration:
                   states["utterance"] = random.choice(potentialUtterance)
                   self.startTime = datetime.datetime.now()
                   # print "Utter:", ConfrontingCall.__name[input["name"]] + "!"
        if self.startTime != None:
            elapsed = datetime.datetime.now() - self.startTime
            if elapsed.seconds > self.__defaultDuration:
                states["utterance"] = ""
                # print "Utter:"
                self.startTime = None
                self.endTime = datetime.datetime.now()

    def itemAction(self, input, agentDistance, potentialUtterance):
        if input.has_key("perceivedItems"):
            for item in input["perceivedItems"]:
                if not item.has_key("orientation"):  # Not an agent but an Item
                    if item["color"]=="blue":
                        color="blau"
                    elif item["color"]=="pink":
                        color="rosate"
                    if item["score"] >= LU_Utter.__minimumSalience:
                        # print item["name"], item["distance"], agentDistance
                        if item["distance"] > agentDistance + LU_Utter.__itemAgentDistance2Approach:
                            potentialUtterance.append(LU_Utter.__name[input["name"]] + ", vade al illo " + color + "!")
                        elif agentDistance > item["distance"] + LU_Utter.__itemAgentDistance2Approach:
                            potentialUtterance.append(LU_Utter.__name[input["name"]] + ", veni al illo " + color + "!")