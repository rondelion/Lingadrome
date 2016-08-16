'''
Created on 2016/08/11

@author: rondelion
'''
import datetime
import random
import math

class LU_Utter(object):
    '''
    classdocs
    '''
    __name = {"BubbleRob#0": "Mario", "BubbleRob#0": "Luca"}
    __defaultDuration = 1 # in seconds
    __suppressDuration = 5 # in seconds
    __judgmentDuration = 3 # in seconds
    __minimumSalience=0.1
    __itemAgentDistance2Approach=0.4
    __approachMargin=0.1
    __pauseMargin=0.05

    def __init__(self):
        '''
        Constructor
        '''
        self.startTime = None
        self.endTime = None
        self.originalDistance = None

    def action(self, input, states, parameters):
        choices = []
        if input.has_key("MSAisInCenterFOV") and input["MSAisInCenterFOV"]:
            if input.has_key("MSAisConfronting") and not input["MSAisConfronting"]:
                choices.append("call")
                choices.append("lookHere")
            if input.has_key("MSAisInConfrontingDistance") and not input["MSAisInConfrontingDistance"]:
                choices.append("comeHere")
            choices.append("pause")
            parameters["utteranceTurnOrientation"] = random.choice(["dextra", "sinistra", ""])
            choices.append("turn")
            self.itemAction(input, parameters, choices)
        if len(choices)>0:
            if self.endTime != None:
                suppressed = datetime.datetime.now() - self.endTime
                if self.startTime == None:
                    self.startTime = self.judgment(suppressed, input, states, parameters)   # may return None
            if self.startTime == None:
                if self.endTime == None or suppressed.seconds > self.__suppressDuration:
                    states["utteranceType"] = random.choice(choices)
                    states["utterance"] = self.choice2utterance(input, states["utteranceType"], parameters)
                    self.startTime = datetime.datetime.now()
                    # print "Utter:", ConfrontingCall.__name[input["name"]] + "!"
        if self.startTime != None:
            elapsed = datetime.datetime.now() - self.startTime
            if elapsed.seconds > self.__defaultDuration:
                states["utterance"] = ""
                states["sanction"] = 0
                # print "Utter:"
                self.startTime = None
                self.endTime = datetime.datetime.now()

    def itemAction(self, input, parameters, choices):
        msa = input["mostSalientAgent"]
        agentDistance = msa["distance"]
        if input.has_key("perceivedItems"):
            for item in input["perceivedItems"]:
                if not item.has_key("orientation"):  # Not an agent but an Item
                    if item["color"]=="blue":
                        parameters["utteranceItemColor"]="blau"
                    elif item["color"]=="pink":
                        parameters["utteranceItemColor"]="rosate"
                    if item["score"] >= LU_Utter.__minimumSalience:
                        # print item["name"], item["distance"], agentDistance
                        if item["distance"] > agentDistance + LU_Utter.__itemAgentDistance2Approach:
                            choices.append("go2Item")
                        elif agentDistance > item["distance"] + LU_Utter.__itemAgentDistance2Approach:
                            choices.append("come2Item")

    def choice2utterance(self, input, choice, parameters):
        if choice == "call":
            return LU_Utter.__name[input["name"]] + "!"
        if choice == "lookHere":
            return LU_Utter.__name[input["name"]] + ", reguarda hic!"
        if choice == "comeHere":
            return LU_Utter.__name[input["name"]] + ", veni hic!"
        if choice == "pause":
            return LU_Utter.__name[input["name"]] + ", resta!"
        if choice == "call":
            return LU_Utter.__name[input["name"]] + "!"
        if choice == "turn":
            return LU_Utter.__name[input["name"]] + ", gira " + parameters["utteranceTurnOrientation"] +"!"
        if choice == "go2Item":
            return LU_Utter.__name[input["name"]] + ", vade al illo " + parameters["utteranceItemColor"] + "!"
        if choice == "come2Item":
            return LU_Utter.__name[input["name"]] + ", veni al illo " + parameters["utteranceItemColor"] + "!"

    def judgment(self, suppressed, input, states, parameters):
        sanction = 0
        msa = input["mostSalientAgent"]
        agentDistance = msa["distance"]
        elapsed = suppressed.seconds
        if elapsed == 0:    # the beginning
            self.originalDistance = agentDistance
        if suppressed.seconds > self.__judgmentDuration:
            if states["utteranceType"]=="comeHere" or states["utteranceType"]=="call":
                if agentDistance < self.originalDistance - self.__approachMargin:
                    sanction = 1
            if states["utteranceType"]=="pause":
                if math.fabs(agentDistance - self.originalDistance) < self.__approachMargin:
                    sanction = 1
            if sanction==1:
                states["utterance"] = "Ben!"
                states["utteranceType"] = "sanction"
                states["sanction"] = sanction
                return datetime.datetime.now()
        return None