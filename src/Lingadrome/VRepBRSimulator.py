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
from VRepBubbleRob import VRepBubbleRob
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
    
    def robPerception(self, rob):
        items=[]
        pos1=rob.getPosition()
        if pos1!=None:
            orientation=rob.getOrientation()
            for br in self.__robs:
                if br!=rob:
                    pos2=br.getPosition()
                    if pos2!=None:
                        item={}
                        ori2=math.atan2(pos2[1]-pos1[1], pos2[0]-pos1[0])-orientation
                        if ori2>math.pi:
                            ori2=ori2-2.0*math.pi
                        item["orientation"]=ori2
                        item["distance"]=math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
                        items.append(item)
                        if self.__cnt % 100==0 and rob.getName()=="BubbleRob#0":
                            print "orientation:", orientation*180.0/math.pi
                            print item["orientation"]*180.0/math.pi
                    else:
                        print >> sys.stderr, "No orientation for " + br.getName()
        else:
            print >> sys.stderr, "No position for " + rob.getName()
        rob.setPerceivedItems(items)

filepath=""

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if argc>=2:
        filepath=argvs[1]
    else:
        print('Indicate following arguments: "file path"!')
        time.sleep(1)
        exit()
    vsim = VRepBRSimulator()
    robs = []   # List of Robs
    fp=open(filepath,'r')
    lines = fp.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
    fp.close()
    for line in lines:
        items = line.split(",")
        for x in items:
            params = x.split(":")
            if len(params)>3:
                try:
                    portNb = int(params[1])
                    clientID=vrep.simxStart("127.0.0.1",portNb,True,True,2000,5)
                    if clientID!=-1:
                        rob = VRepAgent(params[0], clientID, int(params[2]), int(params[3]))
                        vsim.addRob(rob)
                    else:
                        print >> sys.stderr,  "Fatal: No client ID while creating a Bubble Rob."
                except ValueError:
                    print >> sys.stderr,  "Fatal: non integer value while creating a Bubble Rob."
                    time.sleep(1)
                    exit()
    vsim.loop(0.0025)
