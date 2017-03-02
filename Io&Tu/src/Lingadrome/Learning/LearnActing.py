'''
Created on 2016/11/08

@author: rondelion
'''

from Learner import Learner
from Learn import Learn

class LearnActing(Learn):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(LearnActing, self).__init__()
        self.actionLearner = Learner(["turn", "go_away", "come"])

    def learnedAct(self):
        act = self.actionLearner.chooseAction()
        self.learnerLogger("A", self.actionLearner.getContext(), act)
        return act

    def setContext(self, context):
        self.actionLearner.setContext(context)
        self.context = context

    def reward(self, reward):
        self.actionLearner.reward(reward)
        self.rewardLogger("A", self.actionLearner.getContext(), self.actionLearner.getLastAction(), reward)

    def acted(self, action):
        if action == "":
            self.actionLearner.skip()