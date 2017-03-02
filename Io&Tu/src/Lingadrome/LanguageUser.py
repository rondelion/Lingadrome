'''
Created on 2016/11/06

@author: rondelion
'''
from AgentMind import AgentMind
import random

class LanguageUser(AgentMind):
    '''
    classdocs
    '''

    def __init__(self, rad):
        '''
        Constructor
        '''
        super(LanguageUser, self).__init__("User")
        self.states["utterance"] = ""
        self.states["action"] = ""
        self.rewardActDescription = rad

    def selectAction(self): # overriding
        if self.states.has_key("action"):
            self.states["prevAction"] = self.states["action"]
        else:
            self.states["prevAction"] = ""
        if self.states.has_key("utterance"):
            self.states["prevUtterance"] = self.states["utterance"]
        else:
            self.states["prevUtterance"] = ""
        self.states["action"] = ""
        self.states["utterance"] = ""
        self.states["reward"] = 0
        llapp = random.choice(['Tu ', 'Luca '])
        luapp = random.choice(['Io ', 'Mario '])
        llu = self.input["llUtterance"]
        if llu!="" or self.input["llAction"]!="":
            if llu!="":   # if detect LL's utterance
                if llu.startswith('Io ') or llu.startswith('Luca '):
                    if llu.endswith(' gira.'):
                        if self.input["llAction"]=="turn":
                            self.states["reward"] = 1
                    elif llu.endswith(' veni.'):
                        if self.input["llAction"] == "come":
                            self.states["reward"] = 1
                    elif llu.endswith(' vade.'):
                        if self.input["llAction"] == "go_away":
                            self.states["reward"] = 1
                elif llu.startswith('Tu ') or llu.startswith('Mario '):
                    if llu.endswith(' gira.'):
                        if self.states["prevAction"] == "turn":
                            if self.rewardActDescription:
                                self.states["reward"] = 1
                        else:
                            self.states["action"] = "turn"
                            self.states["utterance"] = luapp + "gira."
                    elif llu.endswith(' veni.'):
                        if self.states["prevAction"] == "come":
                            if self.rewardActDescription:
                                self.states["reward"] = 1
                        else:
                            self.states["action"] = "come"
                            self.states["utterance"] = luapp + "veni."
                    elif llu.endswith(' vade.'):
                        if self.states["prevAction"] == "go_away":
                            if self.rewardActDescription:
                                self.states["reward"] = 1
                        else:
                            self.states["action"] = "go_away"
                            self.states["utterance"] = luapp + "vade."
            if self.input["llAction"]!="":  # if detect LL's action
                prvu = ""
                if self.states.has_key("prevUtterance"):
                    prvu = self.states["prevUtterance"]
                if prvu.startswith('Tu ') or prvu.startswith('Luca '):
                    if self.input["llAction"] == "turn" and prvu.endswith(' gira.'):
                        self.states["reward"] = 1
                    elif self.input["llAction"] == "come" and prvu.endswith(' veni.'):
                        self.states["reward"] = 1
                    elif self.input["llAction"] == "go_away" and prvu.endswith(' vade.'):
                        self.states["reward"] = 1
                else:
                    if self.input["llAction"] == "turn":
                        self.states["utterance"] = llapp + "gira."
                    elif self.input["llAction"] == "come":
                        self.states["utterance"] = llapp + "veni."
                    elif self.input["llAction"] == "go_away":
                        self.states["utterance"] = llapp + "vade."
        else:   # command or act
            choice = random.choice(["command","act","none"])
            if choice=="command":
                self.states["action"] = ""
                choices = ["turn", "come", "go_away"]
                choice = random.choice(choices)  # select command randomly
                if choice == "turn":
                    self.states["utterance"] = llapp + "gira."
                elif choice == "come":
                    self.states["utterance"] = llapp + "veni."
                elif choice == "go_away":
                    self.states["utterance"] = llapp + "vade."
            elif choice=="act":   # act and announce
                choices = ["turn", "come", "go_away"]
                choice = random.choice(choices) # select action randomly
                self.states["action"]=choice
                # describe the action
                if choice=="turn":
                    self.states["utterance"] = luapp + "gira."
                elif choice=="come":
                    self.states["utterance"] = luapp + "veni."
                elif choice == "go_away":
                    self.states["utterance"] = luapp + "vade."

