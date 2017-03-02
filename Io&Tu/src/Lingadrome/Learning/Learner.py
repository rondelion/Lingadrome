# -*- coding: utf-8 -*-
'''
Created on 2016/11/15

@author: rondelion
'''

import numpy as np

class Learner(object):
    '''
    classdocs
    '''

    def __init__(self, choices):
        '''
        Constructor
        '''
        self.choices = choices
        self.context = {}
        self.qtable = {}
        self.lastAction = None
        self.totalOccs = 0
        self.choiceOccs = {}
        self.contextItemOccs = {}
        self.contextItemChoiceOccs = {}

    def setContext(self, context):
        self.context = context

    def reward(self, reward):
        if self.lastAction != None:
            self.updateQTable(reward)
            self.updateOccurences(reward)

    def updateQTable(self, reward):
        lastCA = tuple(sorted(self.context.items(), key=lambda x: x[0])) + (self.lastAction,)
        if self.qtable.has_key(lastCA):
            self.qtable[lastCA] = self.qtable[lastCA] + reward
        else:
            self.qtable[lastCA] = reward

    def updateOccurences(self, reward):
        self.totalOccs = self.totalOccs + reward
        if self.choiceOccs.has_key(self.lastAction):
            self.choiceOccs[self.lastAction] = self.choiceOccs[self.lastAction] + reward
        else:
            self.choiceOccs[self.lastAction] = reward
        for key, value in self.context.items():
            kva = (key, value, self.lastAction)
            if self.contextItemOccs.has_key((key, value)):
                self.contextItemOccs[(key, value)] = self.contextItemOccs[(key, value)] + reward
                if self.contextItemChoiceOccs.has_key(kva):
                    self.contextItemChoiceOccs[kva] = self.contextItemChoiceOccs[kva] + reward
                else:
                    self.contextItemChoiceOccs[kva] = reward
            else:
                self.contextItemOccs[(key, value)] = reward
                self.contextItemChoiceOccs[kva] = reward

    def chooseAction(self):
        # print "----------------"
        alphas = self.getAlphasFromQTable()
        # print "Q", alphas
        alphas = self.getAlphasFromNaiveBayes()
        # print "N", alphas
        # generate action from the probabilities
        dd = np.random.dirichlet(tuple(alphas))
        rv = np.random.uniform()
        upper = 0.0
        i = 0
        for x in dd:
            upper = upper + x
            if rv <= upper:
                action = self.choices[i]
                break
            i = i + 1
        self.lastAction = action
        # action = random.choice(self.choices)  # select action randomly
        return action

    def getAlphasFromNaiveBayes(self):
        alphas = []
        # p(choice|context) ∝ (p(choice)/π p(context_item)) * π p(context_item|choice)
        # π p(context_item) = π (occ(context_item) / totalOccs)
        multiOccContext = 1L
        multiTotalOccs = 1L
        minItemOcc = self.totalOccs
        for key, value in self.context.items():
            if self.contextItemOccs.has_key((key, value)):
                multiOccContext = multiOccContext * self.contextItemOccs[(key, value)]
                minItemOcc = min(minItemOcc, self.contextItemOccs[(key, value)])
            multiTotalOccs = multiTotalOccs * self.totalOccs
        p_content_item = 0.0
        if multiTotalOccs!=0:
            p_content_item = float(multiOccContext) / float(multiTotalOccs)
        # for each choice
        content_item_choice_probabilities = []
        sum = 0.0
        for choice in self.choices:
            # π p(context_item|choice) = π(p(context_item,choice)/p(choice))
            # = π(occ(context_item,choice)/occ(choice))
            pContextChoice = 1.0
            multiOccContextChoice = 1L
            multiOccChoice = 1L
            for key, value in self.context.items():
                kvc = (key, value, choice)
                if self.contextItemChoiceOccs.has_key(kvc):
                    multiOccContextChoice = multiOccContextChoice * self.contextItemChoiceOccs[kvc]
                    # print "---"
                    # print "self.contextItemChoiceOccs[kvc]:", kvc, self.contextItemChoiceOccs[kvc]
                    if self.choiceOccs[choice]!=0:
                        multiOccChoice = multiOccChoice * self.choiceOccs[choice]
            pContextChoice = float(multiOccContextChoice) / float(multiOccChoice)
            # p(choice)
            pChoice = 0.0
            if self.choiceOccs.has_key(choice) and self.totalOccs != 0:
                pChoice = float(self.choiceOccs[choice]) / float(self.totalOccs)
            # p(choice|context) ∝ (p(choice)/π p(context_item)) * π p(context_item|choice)
            pChoiceContext = 0.0
            if p_content_item != 0.0:
                pChoiceContext = pChoice * pContextChoice / p_content_item
            content_item_choice_probabilities.append(pChoiceContext)
            sum = sum + pChoiceContext
        i = 0
        for choice in self.choices:
            normalized = 0.0
            if sum != 0:
                normalized = content_item_choice_probabilities[i] / sum
            estOcc = int(normalized * minItemOcc)
            alphas.append(estOcc + 1)
            i = i + 1
        return alphas

    def getAlphasFromQTable(self):
        # get reward probabilities from qTable
        choiceValues = []
        alphas = []
        for choice in self.choices:
            ca = tuple(sorted(self.context.items(), key=lambda x: x[0])) + (choice,)
            if self.qtable.has_key(ca):
                alpha = self.qtable[ca] + 1
                choiceValues.append((choice, self.qtable[ca] + 1))
                alphas.append(alpha)
            else:
                choiceValues.append((choice, 1))
                alphas.append(1)
        # print choiceValues
        return alphas

    def skip(self):
        self.lastAction = None

    def getLastAction(self):
        return self.lastAction

    def getContext(self):
        return self.context
