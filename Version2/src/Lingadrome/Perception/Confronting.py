'''
Created on 2016/07/24

@author: rondelion
'''
import math

class Confronting(object):
    '''
    Detecting the most salient Agent facing each other
    '''
    __score=20   # [0,100]
    __distanceRange=1.0
    __orientationRange=0.1
    __directionRange=0.1

    def __init__(self):
        '''
        Constructor
        '''
        self.__current=False
        self.__previous=False

    def perceive(self, input):
        self.__previous=self.__current
        self.__current=False
        if input.has_key("orientation"):
            if input.has_key("mostSalientAgent"):
                msa=input["mostSalientAgent"]
                if msa!=None and msa.has_key("direction") and \
                    msa.has_key("distance") and msa.has_key("orientation"):
                    msa_dir=msa["direction"]
                    msa_dst=msa["distance"]
                    msa_ori=msa["orientation"]
                    if msa_ori<0.0:
                        rev_msa_ori=math.pi+msa_ori
                    else:
                        rev_msa_ori=msa_ori-math.pi
                    # if input["name"]=="BubbleRob#0":
                    #    print input["orientation"], rev_msa_ori, msa_ori
                    if math.fabs(msa_dir)<Confronting.__directionRange:
                        input["MSAisInCenterFOV"] = True
                    else:
                        input["MSAisInCenterFOV"] = False
                    if math.fabs(input["orientation"]-rev_msa_ori)<Confronting.__orientationRange:
                        input["MSAisConfronting"] = True
                    else:
                        input["MSAisConfronting"] = False
                    if msa_dst<Confronting.__distanceRange:
                        input["MSAisInConfrontingDistance"] = True
                    else:
                        input["MSAisInConfrontingDistance"] = False
