'''
Created on 2016/07/13

@author: rondelion
'''
class Stop(object):
    '''
    classdocs
    '''
    def action(self, input, states, parameters):
        states["steering"]=0.0
        states["thrust"]=0.0
        return
    
    def getName(self):
        return "Stop"
