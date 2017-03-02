#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2016/11/06

@author: rondelion
'''
import sys
from LanguageLearner import LanguageLearner
from LanguageUser import LanguageUser

class Simulator(object):
    '''
    classdocs
    '''
    __cnt=0

    def __init__(self, name, rewardActDescription):
        '''
        Constructor
        '''
        self.logFP = None
        self.ll = LanguageLearner(name)
        self.lu = LanguageUser(rewardActDescription)

    def loop(self, maxLoop):
        llUtt=""
        llAct=""
        while self.__cnt<maxLoop:
            self.__cnt=self.__cnt+1
            self.lu.setInput("llUtterance",llUtt)
            self.lu.setInput("llAction", llAct)
            self.lu.loop()
            luUtt = self.lu.getOutput("utterance")
            luAct = self.lu.getOutput("action")
            luRew = self.lu.getOutput("reward")
            self.ll.setInput("luUtterance",luUtt)
            self.ll.setInput("luAction", luAct)
            self.ll.setReward(luRew)
            self.ll.loop()
            luMode = self.ll.getOutput("mode")
            llUtt = self.ll.getOutput("utterance")
            llAct = self.ll.getOutput("action")
            llRew = self.ll.getOutput("internalReward")
            self.printActivities(luUtt, luAct, luRew, llUtt, llAct, llRew)
        self.logFP.close()

    def printActivities(self, luUtt, luAct, luRew, llUtt, llAct, llRew):
        print >> self.logFP, "[LU Rew]: ", luRew
        print >> self.logFP, "[LU Utt]: ", luUtt
        print >> self.logFP, "[LU Act]: ", luAct
        print >> self.logFP, "[LL Rew]: ", llRew
        print >> self.logFP, "[LL Utt]: ", llUtt
        print >> self.logFP, "[LL Act]: ", llAct

    def setLogFile(self, path):
        try:
            self.logFP = open(path,'w')
        except:
            print >> sys.stderr, "Fatal: error opening the log file."
            exit()

    def setRewardLog(self, path):
        rewardLog = None
        try:
            rewardLog = open(path,'w')
        except:
            print >> sys.stderr, "Fatal: error opening the reward log file."
            exit()
        self.ll.setRewardLog(rewardLog)

    def setLearnerLog(self, path):
        learnerLog = None
        try:
            learnerLog = open(path,'w')
        except:
            print >> sys.stderr, "Fatal: error opening the learner log file."
            exit()
        self.ll.setLearnerLog(learnerLog)

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if argc!= 6:
        print "Simulator maxLoop switch logfile rewardLog learnerLog"
        print "switch1: N iff Use agent names"
        print "switch2: 1 iff Give reward for utterances describing LU's action"
    maxLoop=int(argvs[1])
    name = False
    if argvs[2][0]=="N":
        name = True
    rewardActDescription = False
    if argvs[2][1]=="1":
        rewardActDescription = True
    sim = Simulator(name, rewardActDescription)
    sim.setLogFile(argvs[3])
    sim.setRewardLog(argvs[4])
    sim.setLearnerLog(argvs[5])
    sim.loop(maxLoop)
