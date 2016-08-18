'''
Created on 2016/07/13

@author: rondelion
'''
class Turn(object):
    '''
    classdocs
    '''
    def action(self, input, states, parameters):
        steering=0.2
        if parameters.has_key("turnDirection"):
            if parameters["turnDirection"]=="L":
                steering=steering * -1.0
        states["thrust"]=0.0
        states["steering"]=steering
        # if parameters.has_key("turnDirection") and parameters["turnDirection"]=="L":
        #    print "Turn", states["steering"]
        return
    
    def getName(self):
        return "Turn"
