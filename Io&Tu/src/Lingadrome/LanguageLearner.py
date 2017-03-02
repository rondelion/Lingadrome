'''
Created on 2016/11/06

@author: rondelion
'''
from AgentMind import AgentMind
from Learning.LearnUttering import LearnUttering
from Learning.LearnActing import LearnActing
import random
import sys

class LanguageLearner(AgentMind):
    '''
    classdocs
    '''

    def __init__(self, name):
        '''
        Constructor
        '''
        super(LanguageLearner, self).__init__("Learner")
        self.learnUttering = LearnUttering(name)
        self.learnActing = LearnActing()
        self.lastAction = ""

    # All action is performed via reinforcement learning
    def selectAction(self):  # overriding
        self.states["utterance"] = ""
        self.states["action"] = ""
        self.states["command"] = ""
        if self.input["luUtterance"]!="" or self.input["luAction"]!="":
            self.states["mode"] = "react"
            if self.lastAction == "":
                if self.input["luUtterance"]!="":   # if detect LU's utterance
                    if self.input["luAction"] == "":  # if not detect LU's action
                        self.setContext4Acting()
                        self.states["action"] = self.learnActing.learnedAct()
                    else:
                        self.setContext4Uttering()
                        self.states["utterance"] = self.learnUttering.learnedUtterance()
        else:   # act and announce
            choice = random.choice(["command","act","none"])
            self.states["mode"] = choice
            if choice=="command":
                choices = ["turn", "come", "go_away"]
                choice = random.choice(choices)  # select command randomly
                self.states["command"]=choice
                self.setContext4Uttering()
                self.states["utterance"] = self.learnUttering.learnedUtterance()
            elif choice=="act":
                choices = ["turn", "come", "go_away"]
                choice = random.choice(choices) # select action randomly
                self.states["action"]=choice
                # describe the action
                self.setContext4Uttering()
                self.states["utterance"] = self.learnUttering.learnedUtterance()
        self.lastAction = self.states["action"]
        self.learnUttering.uttered(self.states["utterance"])
        self.learnActing.acted(self.states["action"])

    def setReward(self, reward):
        self.states["internalReward"] = 0
        if self.states.has_key("mode") and self.states["mode"] == "command" and reward==0:
            if self.states["command"] == self.input["luAction"]:    # Internal Reward
                reward = 1
                self.states["internalReward"] = 1
        self.learnUttering.setCount(self.count)
        self.learnActing.setCount(self.count)
        self.learnUttering.reward(reward)
        self.learnActing.reward(reward)

    def setContext4Acting(self):
        context = {}
        if self.input.has_key("luUtterance") and self.input["luUtterance"]!="":
            luWords = self.input["luUtterance"].strip('.').split()
            context["luWord1"] = luWords[0]
            context["luWord2"] = luWords[1]
            context["LUU"] = True  # LU Uttering
        else:
            context["luWord1"] = ""
            context["luWord2"] = ""
            context["LUU"] = False
        if self.states.has_key("utterance") and self.states["utterance"]!="":
            llWords = self.states["utterance"].strip('.').split()
            context["llWord1"] = llWords[0]
            context["llWord2"] = llWords[1]
            context["SOU"] = True   # Sense of Utterance
        else:
            context["llWord1"] = ""
            context["llWord2"] = ""
            context["SOU"] = False
        self.learnActing.setContext(context)

    def setContext4Uttering(self):
        context = {}
        if self.input.has_key("luAction") and self.input["luAction"] != "":
            context["luAction"] = self.input["luAction"]
            # context["LUA"] = True  # LU Acting
        else:
            context["luAction"] = ""
            # context["LUA"] = False
        if self.states.has_key("action") and self.states["action"] != "":
            context["llAction"] = self.states["action"]
            # context["SOA"] = True  # Sense of Agency
        else:
            context["llAction"] = ""
            # context["SOA"] = False
        context["mode"] = self.states["mode"]
        context["command"] = self.states["command"]
        self.learnUttering.setContext(context)

    def setRewardLog(self, fp):
        self.learnUttering.setRewardLog(fp)
        self.learnActing.setRewardLog(fp)

    def setLearnerLog(self, fp):
        self.learnUttering.setLearnerLog(fp)
        self.learnActing.setLearnerLog(fp)