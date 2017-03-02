'''
Created on 2016/11/16

@author: rondelion
'''

class Learn(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.context = {}
        self.rewardLog = None
        self.learnerLog = None
        self.count = 0

    def setContext(self, context):
        self.context = context

    def setRewardLog(self, fd):
        self.rewardLog = fd

    def setLearnerLog(self, fd):
        self.learnerLog = fd

    def setCount(self, cnt):
        self.count = cnt

    def rewardLogger(self, type, context, act, reward):
        if self.rewardLog!=None:
            mode = context.get("mode", "")
            if act != None:
                print >> self.rewardLog, str(self.count) + "\t" + type + "\t" + mode + "\t" + act + "\t" + str(reward)

    def learnerLogger(self, type, context, act):
        if self.learnerLog!=None:
            cxt = sorted(context.items(), key=lambda x: x[0])
            cbf = ""
            for x in cxt:
                cbf = cbf + x[0] + ":" + str(x[1]) + ","
            print >> self.learnerLog, type + ":" + act + "," + cbf