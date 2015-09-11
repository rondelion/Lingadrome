#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015/09/08

@author: rondelion
'''

# Make sure to have the server side running in V-REP!
# Start the server from a child script with following command:
# simExtRemoteApiStart(portNumber) -- starts a remote API server service on the specified port

import sys
import time
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
    '''
try:
    import vrepConst
except:
    print ('"vrepConst.py" could not be imported.')
    exit(-1)
    '''

class VRepBRSimulator(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if argc>=3:
        portNb=int(argvs[1])
        worldFileName=argvs[2]
    else:
        print('Indicate following arguments: "portNumber"!')
        time.sleep(1)
        exit()
    # Read the World file
    # Create the World object
    # world=World(worldFileName)
    # relate world objects to V-Rep objects 
    clientID=vrep.simxStart("127.0.0.1",portNb,True,True,2000,5)
    if clientID!=-1:
        driveBackStartTime=-99000
        while vrep.simxGetConnectionId(clientID)!=-1:
            time.sleep(0.005)
            # Get information from V-Rep
            # Send information to V-Rep
        vrep.simxFinish(clientID)

