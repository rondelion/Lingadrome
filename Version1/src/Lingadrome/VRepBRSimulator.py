#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015/10/12

@author: rondelion
'''
import sys
import os
import time
import math
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
    __cnt=0

    def __init__(self):
        '''
        Constructor
        '''
        self.__clientID=0

    def setClientID(self, clientID):
        self.__clientID=clientID
        
    def getClientID(self):
        return self.__clientID
        
    def addRob(self, rob):
        self.__robs.append(rob)
    
    def addItem(self, item):
        self.__items.append(item)
        
    def loop(self, interval):
        while vrep.simxGetConnectionId(self.getClientID())!=-1:
            self.__cnt=self.__cnt+1
            for rob in self.__robs:
                rob.loop()
                self.robPerception(rob)
                # print rob.getName(), rob.getPosition()
            for item in self.__items:
                item.loop()
            time.sleep(interval)
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
        
    def waitForDummyPathUpdate(self, path):
        cnt=0
        mtime = os.stat(path).st_mtime
        while os.stat(path).st_mtime==mtime:
            time.sleep(0.1)
            cnt=cnt+1
            if cnt>100:
                print >> sys.stderr,  "Aborted! Did not detect server activity within 10 seconds."
                time.sleep(1)
                exit()
        
    def robPerception(self, rob):
        vrobjs=[]
        pos1=rob.getPosition()
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
                        vrobj["emotion"] = self.getEmotion(br)
                        vrobjs.append(vrobj)
                    else:
                        print >> sys.stderr, "No position obtained for " + br.getName()
            # item perception
            for item in self.__items:
                vrobj={}
                pos2=item.getPosition()
                if pos2!=None:
                    vrobj["direction"]=self.__getDirection(pos1, pos2, orientation)
                    vrobj["distance"]=math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
                    vrobj["name"]=item.getName()
                    vrobjs.append(vrobj)
                else:
                    print >> sys.stderr, "No position obtained for " + item.getName()
        else:
            print >> sys.stderr, "No position for " + rob.getName()
        rob.setPerceivedItems(vrobjs)

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
    vsim.waitForDummyPathUpdate(dummyPath)
    # LingadromeDummy.txt
    fp=open(dummyPath,'r')
    lines = fp.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
    fp.close()
    for line in lines:
        buf = line.split(",")
        for x in buf:
            params = x.split(":")
            if len(params)>=2:
                name=params[0]
                try:
                    portNb = 19998  # int(params[1])
                    dummyID=vrep.simxStart("127.0.0.1",portNb,True,True,2000,5)
                    if dummyID==-1:
                        print >> sys.stderr,  "Fatal: No client ID while creating Dummy Communicator."
                    else:
                        vsim.setClientID(dummyID)
                except ValueError:
                    print >> sys.stderr,  "Fatal: non integer value while creating Dummy Communicator."
                    time.sleep(1)
                    exit()
            else:
                name=params[0]
                returnCode, handle = vrep.simxGetObjectHandle(dummyID, name, vrep.simx_opmode_oneshot_wait)
                if returnCode!=vrep.simx_return_ok:
                    print >> sys.stderr,  "Fatal: Error obtaining a handle for " + name + "!"
                else:
                    print name, handle
                    item = VRepItem(name, dummyID, handle)
                    vsim.addItem(item)
    # RobParts.txt
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
                    rob.setCarryingDirection(0.27*math.pi)  # (random.random()-0.5)*2.0*math.pi) # radian
                    vsim.addRob(rob)
                except ValueError:
                    print >> sys.stderr,  "Fatal: non integer value while creating a Bubble Rob."
                    time.sleep(1)
                    exit()
    vsim.loop(0.0025)
