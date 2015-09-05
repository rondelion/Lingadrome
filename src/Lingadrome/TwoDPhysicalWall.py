'''
Created on 2015/09/05

@author: rondelion
'''

class TwoDWall(object):
    '''
    classdocs
    '''
    __beginLoc=(0.0,0.0)
    __endLoc=(0.0,0.0)


    def __init__(self, begin, end):
        '''
        Constructor
        '''
        self.__beginLoc=begin
        self.__endLoc=end

        