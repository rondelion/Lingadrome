# -*- coding: utf-8 -*-
'''
Created on 2015/08/28

@author: rondelion
'''
from VRepObject import VRepObject

class VRepItem(VRepObject):
    '''
    classdocs
    '''


    def __init__(self, name, clientID, handle):
        '''
        Constructor
        '''
        self.__name=name
        self.__clientID=clientID    # Client ID of the Dummy object
        self.__handle=handle        # VRep object handle
        