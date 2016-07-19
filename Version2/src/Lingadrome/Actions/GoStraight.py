'''
Created on 2016/07/13

@author: rondelion
'''
class GoStraight(object):
    '''
    classdocs
    '''
    def action(self, input, states, parameters):
        thrust=1.0
        steering=0.0
        if input.has_key("velocity") and input["velocity"]>0.03:
            thrust=0.0
        states["steering"]=steering
        states["thrust"]=thrust
        return
    
    def getName(self):
        return "GoStraight"
