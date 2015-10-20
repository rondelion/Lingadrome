'''
Created on 2015/10/20

@author: rondelion
'''

class Rule(object):
    '''
    classdocs
    '''
    __score=0   # [0,100]

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def condition(self, inputBuffer, stateBuffer):
        return False
    
    def action(self, inputBuffer, stateBuffer):
        return {}   # Empty return buffer dictionary
    
    def getName(self):
        return "default"
    
    def getScore(self):
        return self.__score