'''
Created on 2016/07/21

@author: rondelion
'''
from AgentMind2 import AgentMind2
from Actions.LU_Utter import LU_Utter

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
        if self.input.has_key("mostSalientAgent"):
            msa = self.input["mostSalientAgent"]
            if msa!=None and msa.has_key("direction"):
                self.states["locomotionType"] = "Turn"
                if msa["direction"] > 0:
                    self.actionParameters["turnDirection"] = "L"
                else:
                    self.actionParameters["turnDirection"] = "R"
        self.lu_Utter.action(self.input, self.states, self.actionParameters)
