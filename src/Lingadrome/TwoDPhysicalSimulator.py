'''
Created on 2015/09/05

@author: rondelion
'''
from math import sqrt

class TwoDPhysicalSimulator(object):
    '''
    classdocs
    '''
    __step=0.0  # second
    __walls={}
    __objects={}

    def __init__(self, step):
        '''
        Constructor
        '''
        self.__step=step
        
    def addWall(self, handle, wall):
        self.__walls[handle]=wall
        
    def addObject(self, handle, twoDObject):
        self.__objects[handle]=twoDObject
    
    def getObject(self, handle):
        return self.__objects[handle]
    
    def detectCollision(self, hdl1):
        collisionTable={}
        for hdl2 in self.__objects:
            if not hdl1==hdl2:
                # Ref. http://www.geisya.or.jp/~mwm48961/math2/quad_eq_episode1.htm
                loc1=self.__objects[hdl1].getLocation()
                loc2=self.__objects[hdl2].getLocation()
                locDiff = (loc1[0]-loc2[0],loc1[1]-loc2[1])
                v1=self.__objects[hdl1].getVelocity()
                v2=self.__objects[hdl2].getVelocity()
                vDiff = (v1[0]-v2[0],v1[1]-v2[1])
                vDiffSq = vDiff[0]**2+vDiff[1]**2
                if vDiffSq==0:  # never cross the same speed
                    continue
                a=vDiff[0]**2+vDiff[1]**2
                b=(locDiff[0]*vDiff[0]+locDiff[1]*vDiff[1])*2.0
                c=locDiff[0]**2+locDiff[1]**2-self.__objects[hdl1].getRadius()**2-self.__objects[hdl2].getRadius()**2
                rtDiffSq = b**2-4.0*a*c
                if rtDiffSq < 0:
                    pass    # never cross
                else:
                    t1 = (-1.0*b - sqrt(rtDiffSq))/vDiffSq
                    t2 = (-1.0*b + sqrt(rtDiffSq))/vDiffSq
                    if t1>=0 and t1 <= self.__step:
                        collisionTable[hdl2]=t1
                    elif t2>=0 and t2 <= self.__step:
                        collisionTable[hdl2]=t2
                
        # TODO: Collision with wall
        # TODO: Multiple Collisions
        # TODO: Course change by collisions
    
    def elapse(self):
        # let the step period pass in which the velocities are constant
        for handle in self.__objects:
            obj=self.__objects[handle]
            if self.detectCollision(handle):
                pass    # TODO:
            else:
                obj.setLocation=(obj.getLocation[0]+obj.getVelocity[0]*self.__step, obj.getLocation[1]+obj.getVelocity[1]*self.__step)
                obj.setVelocity=(obj.getVelocity[0]+obj.getAcceleration[0]*self.__step, obj.getVelocity[1]+obj.getAcceleration[1]*self.__step)
    