'''
Created on 2016/11/08

@author: rondelion
'''

from Learner import Learner
from Learn import Learn
import random

class LearnUttering(Learn):
    '''
    classdocs
    '''

    def __init__(self, name):
        '''
        Constructor
        '''
        super(LearnUttering, self).__init__()
        if name:
            self.subjectLemmaLearner = Learner(["S1", "S2", "S3", "S4"])
        else:
            self.subjectLemmaLearner = Learner(["S1", "S2"])
        self.verbLemmaLearner = Learner(["V1", "V2", "V3"])

    def learnedUtterance(self):
        subjLemma = self.subjectLemmaLearner.chooseAction()
        self.learnerLogger("S", self.subjectLemmaLearner.getContext(), subjLemma)
        if subjLemma == "S1":
            subj = "Io"
        elif subjLemma == "S2":
            subj = "Tu"
        elif subjLemma == "S3":
            subj = "Luca"
        elif subjLemma == "S4":
            subj = "Mario"
        verbLemma = self.verbLemmaLearner.chooseAction()
        self.learnerLogger("V", self.verbLemmaLearner.getContext(), verbLemma)
        if verbLemma == "V1":
            verb = "gira"
        elif verbLemma == "V2":
            verb = "veni"
        else:
            verb = "vade"
        return subj + " " + verb + "."

    def setContext(self, context):
        self.subjectLemmaLearner.setContext(context)
        self.verbLemmaLearner.setContext(context)
        self.context = context

    def reward(self, reward):
        self.subjectLemmaLearner.reward(reward)
        self.verbLemmaLearner.reward(reward)
        self.rewardLogger("S", self.subjectLemmaLearner.getContext(), self.subjectLemmaLearner.getLastAction(), reward)
        self.rewardLogger("V", self.verbLemmaLearner.getContext(), self.verbLemmaLearner.getLastAction(), reward)

    def uttered(self, utterance):
        if utterance == "":
            self.subjectLemmaLearner.skip()
            self.verbLemmaLearner.skip()
