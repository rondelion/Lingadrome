'''
Created on 2016/07/24

@author: rondelion
'''

from Confronting import Confronting

class Perceive(object):
    '''
    classdocs
    '''
    __score = 0  # [0,100]

    def __init__(self):
        '''
        Constructor
        '''
        self.confronting = Confronting()

    def perceive(self, input, states):
        self.confronting.perceive(input)