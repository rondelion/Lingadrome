#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015/10/12

@author: rondelion
'''
import sys
import time
import math
from VRepAgent import VRepAgent
try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')
    exit(-1)

class VRepBRSimulator(object):
    '''
    classdocs
    '''
    __robs=[]
    __cnt=0

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def addRob(self, rob):
        self.__robs.append(rob)
    
    def loop(self, interval):
        while True:
            self.__cnt=self.__cnt+1
            for rob in self.__robs:
                if vrep.simxGetConnectionId(rob.getClientID())!=-1:
                    rob.loop()
                    self.robPerception(rob)
                    # print rob.getName(), rob.getPosition()
                else:
                    print >> sys.stderr,  "Fatal: cannot connect with a Bubble Rob."
                    time.sleep(1)
                    exit()
            time.sleep(interval)        
    
    def getEmotion(self, rob):
        ok, val = vrep.simxGetIntegerSignal(rob.getClientID(), rob.getName()+":Emotion", vrep.simx_opmode_streaming)
        if ok==vrep.simx_return_ok:
            return val
        else:
            return 0    # neutral emotion

    def robPerception(self, rob):
        items=[]
        pos1=rob.getPosition()
        if pos1!=None:
            orientation=rob.getOrientation()
            for br in self.__robs:
                if br!=rob:
                    item={}
                    pos2=br.getPosition()
                    if pos2!=None:
                        direction=math.atan2(pos2[1]-pos1[1], pos2[0]-pos1[0])-orientation
                        if direction>math.pi:
                            direction=direction-2.0*math.pi
                        if direction<-1.0*math.pi:
                            direction=2.0*math.pi+direction
                        # if rob.getName()=="BubbleRob#1":
                        #    print direction, math.atan2(pos2[1]-pos1[1], pos2[0]-pos1[0]), orientation
                        item["direction"]=direction
                        item["distance"]=math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
                        item["name"]=br.getName()
                        brOri=br.getOrientation()
                        if brOri!=None:
                            item["orientation"]=brOri
                        # if self.__cnt % 100==0 and rob.getName()=="BubbleRob#1":
                        #    print "self-orientation:", orientation, "diff-orientation:", direction
                    else:
                        print >> sys.stderr, "No orientation for " + br.getName()
                    item["emotion"]=self.getEmotion(br)
                    items.append(item)
        else:
            print >> sys.stderr, "No position for " + rob.getName()
        rob.setPerceivedItems(items)

robParts=""
dummyPath=""
dummyID=-1

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if argc>=3:
        dummyPath=argvs[1]
        robParts=argvs[2]
    else:
        print('Specify following arguments: "dummyPath robParts"!')
        time.sleep(1)
        exit()
    vsim = VRepBRSimulator()
    items=[]    # List of Items
    fp=open(dummyPath,'r')
    lines = fp.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
    fp.close()
    for line in lines:
        items = line.split(",")
        for x in items:
            print x
            params = x.split(":")
            if len(params)>=2:
                name=params[0]
                try:
                    portNb = int(params[1])
                    dummyID=vrep.simxStart("127.0.0.1",portNb,True,True,2000,5)
                    if dummyID!=-1:
                        returnCode, handle = vrep.simxGetObjectHandle(dummyID, "Dummy", vrep.simx_opmode_oneshot_wait)
                        print dummyID, returnCode, handle
                    else:
                        print >> sys.stderr,  "Fatal: No client ID while creating Dummy Communicator."
                except ValueError:
                    print >> sys.stderr,  "Fatal: non integer value while creating Dummy Communicator."
                    time.sleep(1)
                    exit()
    robs = []   # List of Robs
    fp=open(robParts,'r')
    lines = fp.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
    fp.close()
    for line in lines:
        buf = line.split(",")
        for x in buf:
            params = x.split(":")
            if len(params)>2:
                try:
                    rob = VRepAgent(params[0], dummyID, int(params[1]), int(params[2]))
                    vsim.addRob(rob)
                except ValueError:
                    print >> sys.stderr,  "Fatal: non integer value while creating a Bubble Rob."
                    time.sleep(1)
                    exit()
    vsim.loop(0.0025)
