'''
Created on 2016/07/21

@author: rondelion
'''
from AgentMind2 import AgentMind2
from Actions.LU_Utter import LU_Utter
import random

class LanguageUser(AgentMind2):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(LanguageUser, self).__init__("User")
        self.lu_Utter = LU_Utter()

    def selectAction(self): # overriding
        self.states["locomotionType"] = "Stop"
        self.lu_Utter.action(self.input, self.states, self.actionParameters)
        if self.states.has_key("utteranceType"):
            if self.states["utteranceType"]=="approaching":
                self.states["locomotionType"] = "Approach"
            elif self.states["utteranceType"]=="turning":
                self.states["locomotionType"] = "Turn"
                if self.actionParameters.has_key("announceTurnOrientation"):
                    if self.actionParameters["announceTurnOrientation"]=="sinistra":
                        self.actionParameters["turnDirection"] = "L"
                    elif self.actionParameters["announceTurnOrientation"]=="dextra":
                        self.actionParameters["turnDirection"] = "R"
                    else:
                        self.actionParameters["turnDirection"] = random.choice(["L","R"])
            else:
                self.defaultTracking()
        else:
            self.defaultTracking()

    def defaultTracking(self):
        if self.input.has_key("mostSalientAgent"):
            msa = self.input["mostSalientAgent"]
            if msa != None and msa.has_key("direction"):
                self.states["locomotionType"] = "Turn"
                if msa["direction"] > 0:
                    self.actionParameters["turnDirection"] = "L"
                else:
                    self.actionParameters["turnDirection"] = "R"