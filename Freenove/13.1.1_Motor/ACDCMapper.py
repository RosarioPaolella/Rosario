#!/usr/bin/env python3
########################################################################
# Filename    : ADCDMapper.py
# Description : ACDC [0..255] mapper values
# Author      : Rosario Paolella
# modification: 2021/02/14
########################################################################
            
class ADCDMapper(object):
    values=[0]*256    

    def SetMapping(self,init,end,val):
        if init<=end : 
            x1=init
            x2=end
        else:
            x1=end
            x2=init
        
        for i in range (x1,x2):
            self.values[i]=val
    
    def GetMappedValue(self,index):
        return self.values[index]