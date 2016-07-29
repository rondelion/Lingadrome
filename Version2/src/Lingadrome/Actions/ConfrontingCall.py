'''
Created on 2016/07/24

@author: rondelion
'''
import datetime

class ConfrontingCall(object):
    '''
    classdocs
    '''
    __name = {"BubbleRob#0": "Mario", "BubbleRob#0": "Luca"}
    __defaultDuration = 1 # in seconds
    __suppressDuration = 5 # in seconds

    def __init__(self):
        '''
        Constructor
        '''
        self.startTime = None
        self.endTime = None

    def action(self, input, states, parameters):
        if input.has_key("MSAisInCenterFOV") and input.has_key("MSAisConfronting") \
                and input["MSAisInCenterFOV"] and not input["MSAisConfronting"]:
            if self.endTime != None:
                suppressed = datetime.datetime.now() - self.endTime
            if self.startTime == None:
               if self.endTime == None or suppressed.seconds > self.__suppressDuration:
                   states["utterance"] = ConfrontingCall.__name[input["name"]] + "!"
                   self.startTime = datetime.datetime.now()
                   # print "Utter:", ConfrontingCall.__name[input["name"]] + "!"
        if self.startTime != None:
            elapsed = datetime.datetime.now() - self.startTime
            if elapsed.seconds > self.__defaultDuration:
                states["utterance"] = ""
                # print "Utter:"
                self.startTime = None
                self.endTime = datetime.datetime.now()
