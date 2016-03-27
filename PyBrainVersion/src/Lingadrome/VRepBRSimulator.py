#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015/10/12
PyBrain version 2016-02-11
@author: rondelion
'''
import sys
import os
import time
import math
import random
from VRepAgent import VRepAgent
from VRepItem import VRepItem
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
    __items=[]

    def __init__(self):
        '''
        Constructor
        '''
        self.__clientID=0
        self.dummyPath=""
        self.dummyID=None
        self.robParts=""
        self.maxLoop=100
        self.learnLoop=100

    def setClientID(self, clientID):
        self.__clientID=clientID
        
    def getClientID(self):
        return self.__clientID
        
    def addRob(self, rob):
        self.__robs.append(rob)
    
    def addItem(self, item):
        self.__items.append(item)
        
    def learningLoop(self):
        cnt=0
        while cnt<self.maxLoop:
            self.loop(0.0025, True, self.learnLoop)
            for rob in self.__robs:
                rob.setCarryingDirection(0.0) # (random.random()-0.5)*2.0*math.pi) # radian
                rob.pybrainLearn()
                rob.pybrainReset()
            self.resetSimulation()
            cnt+=1

    def loop(self, interval, learning, learnLoop):
        cnt=0
        while vrep.simxGetConnectionId(self.getClientID())!=-1 and ((not learning) or cnt<learnLoop):
            for item in self.__items:
                item.loop()
            for rob in self.__robs:
                rob.observe()
                self.robPerception(rob)
                if cnt>1:
                    rob.setRewards()
                # print rob.getLastAction()
                rob.act()
                # print rob.getName(), rob.getPosition()
            time.sleep(interval)
            cnt+=1
        if vrep.simxGetConnectionId(self.getClientID())==-1:
            print >> sys.stderr,  "Disconnected: Exiting from the main loop!"
            time.sleep(1)
            exit()
    
    def getEmotion(self, rob):
        ok, val = vrep.simxGetIntegerSignal(self.getClientID(), rob.getName()+":Emotion", vrep.simx_opmode_streaming)
        if ok==vrep.simx_return_ok:
            return val
        else:
            return 0    # neutral emotion

    def __getDirection(self, pos1, pos2, orientation):
        direction=math.atan2(pos2[1]-pos1[1], pos2[0]-pos1[0])-orientation
        if direction>math.pi:
            direction=direction-2.0*math.pi
        if direction<-1.0*math.pi:
            direction=2.0*math.pi+direction
        return direction
        
    def waitForDummyPathUpdate(self):
        cnt=0
        mtime = os.stat(self.dummyPath).st_mtime
        while os.stat(self.dummyPath).st_mtime==mtime:
            time.sleep(0.1)
            cnt=cnt+1
            if cnt>100:
                print >> sys.stderr,  "Aborted! Did not detect server activity within 10 seconds."
                time.sleep(1)
                exit()
        
    def readDummyPath(self):
        fp = open(self.dummyPath, 'r')
        lines = fp.readlines()  # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
        fp.close()
        for line in lines:
            buf = line.split(",")
            for x in buf:
                params = x.split(":")
                if len(params) >= 2:
                    name = params[0]
                    try:
                        portNb = 19998 # int(params[1])
                        self.dummyID = vrep.simxStart("127.0.0.1", portNb, True, True, 2000, 5)
                        if self.dummyID == -1:
                            print >> sys.stderr, "Fatal: No client ID while creating Dummy Communicator."
                        else:
                            self.setClientID(self.dummyID)
                    except ValueError:
                        print >> sys.stderr, "Fatal: non integer value while creating Dummy Communicator."
                        time.sleep(1)
                        exit()
                else:
                    name = params[0]
                    returnCode, handle = vrep.simxGetObjectHandle(self.dummyID, name, vrep.simx_opmode_oneshot_wait)
                    if returnCode != vrep.simx_return_ok:
                        print >> sys.stderr, "Fatal: Error obtaining a handle for " + name + "!"
                    else:
                        print name, handle
                        item = VRepItem(name, self.dummyID, handle)
                        self.addItem(item)
        
    def readRobParts(self):
        fp=open(self.robParts,'r')
        lines = fp.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
        fp.close()
        for line in lines:
            buf = line.split(",")
            for x in buf:
                params = x.split(":")
                if len(params)>2:
                    try:
                        rob = VRepAgent(params[0], self.dummyID, int(params[1]), int(params[2]))
                        vsim.addRob(rob)
                    except ValueError:
                        print >> sys.stderr,  "Fatal: non integer value while creating a Bubble Rob."
                        time.sleep(1)
                        exit()
    
    def robPerception(self, rob):
        pos1=rob.getPosition()
        vragents=[]
        if pos1!=None:
            orientation=rob.getOrientation()
            # other agent perception
            for br in self.__robs:
                if br!=rob:
                    vrobj={}
                    pos2=br.getPosition()
                    if pos2!=None:
                        vrobj["direction"]=self.__getDirection(pos1, pos2, orientation)
                        vrobj["distance"]=math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
                        vrobj["name"]=br.getName()
                        brOri=br.getOrientation()
                        if brOri!=None:
                            vrobj["orientation"]=brOri
                    else:
                        print >> sys.stderr, "No position obtained for " + br.getName()
                    vrobj["emotion"]=self.getEmotion(br)
                    vragents.append(vrobj)
                    rob.setPerceivedAgents(vragents)
            # item perception
            vritems=[]
            for item in self.__items:
                vrobj={}
                pos2=item.getPosition()
                if pos2!=None:
                    vrobj["direction"]=self.__getDirection(pos1, pos2, orientation)
                    vrobj["distance"]=math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
                    vrobj["name"]=item.getName()
                else:
                    print >> sys.stderr, "No position obtained for " + item.getName()
                vritems.append(vrobj)
                rob.setPerceivedItems(vritems)
        else:
            print >> sys.stderr, "No position for " + rob.getName()

    def resetSimulation(self):
        returnCode = vrep.simx_return_novalue_flag
        while returnCode!=vrep.simx_return_ok:
            returnCode=vrep.simxStopSimulation(self.__clientID, vrep.simx_opmode_oneshot)
            time.sleep(0.5)
        time.sleep(0.5)
        returnCode = vrep.simx_return_novalue_flag
        while returnCode!=vrep.simx_return_ok:
            returnCode=vrep.simxStartSimulation(self.__clientID, vrep.simx_opmode_oneshot)
            time.sleep(0.5)
        
    def resetPositions(self):
        # reset item positions
        for item in self.__items:
            item.returnToInitPosition()

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    vsim = VRepBRSimulator()
    if argc>=5:
        vsim.dummyPath=argvs[1]
        vsim.robParts=argvs[2]
        vsim.maxLoop=int(argvs[3])
        vsim.learnLoop=int(argvs[4])
    else:
        print('Specify following arguments: "dummyPath robParts maxLoop learnLoop"!')
        time.sleep(1)
        exit()
    vsim.waitForDummyPathUpdate()
    # LingadromeDummy.txt
    vsim.readDummyPath()
    # RobParts.txt
    vsim.readRobParts()
    vsim.learningLoop()
