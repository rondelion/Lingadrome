'''
Created on 2016/07/13

@author: rondelion
'''
class Approach(object):
    '''
    classdocs
    '''
    def action(self, input, states, parameters):
        steering=0.2
        if states.has_key("target"):
            target = states["target"]
            item = self.selectPerceivedObject(input, states["target"])
            # print item["name"], item["direction"]
            if item.has_key("direction"):
                if item["direction"] > 0:
                    steering = steering * -1.0
        states["thrust"]=0.5
        states["steering"]=steering


    def selectPerceivedObject(self, input, name):
        if input.has_key("perceivedItems"):
            for item in input["perceivedItems"]:
                if item["name"] == name:
                    return item
        else:
            return None