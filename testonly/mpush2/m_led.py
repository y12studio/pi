#
# Copyright 2013 Y12Studio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import  m_dys388icon as ledicon
import  m_dys388dbp as ledDys388
import numpy as np
import threading,time

_lastWriteLed = -1
_flagNewEvt = False
_flagRun = True

_stdDevTotal = 0
_stdDev3x3 = []

class AnimLed:
    def __init__(self, animArr):
        self.animArr = animArr
        self.runflag = False
        self.count = 0
        self.color = ledDys388.colorR
        self.code = 0
        self.t = None
        
    def _animWorker(self):
        self.runflag = True
        while self.runflag:
            i = self.count % len(self.animArr)
            v =  self.animArr[i]
            ledDys388.write(self.color, v)
            time.sleep(0.2)
            self.count+=1
    
    def smile(self):
        if self.code != 0:
            if self.runflag:
                self.stop()        
            ledDys388.write(ledDys388.colorG, ledicon.faceSmile)
            self.code = 0
    
    def anim(self):
        self.code = 1
        if self.t != None:
            pass
        else :
            ledDys388.clear()
            self.code = 1
            self.t = threading.Thread(target=self._animWorker)
            self.t.start()
            
    def setColor(self,c):
        if c != self.color:
            ledDys388.clear()
            self.color = c
        
    def stop(self):
        self.runflag = False
        ledDys388.clear()
        self.t = None


class CircleLed:
    def __init__(self, animArr):
        self.animArr = animArr
        self.runflag = False
        self.newEvt = False
        self.idle = False
        self.count = 0
        self.color = ledDys388.colorR
        self.index = 0
        self.t = threading.Thread(target=self._animWorker)
        self.t.start()
        
    def stop(self):
        self.runflag = False
        ledDys388.clear()
        
    def _animWorker(self):
        self.runflag = True
        while self.runflag:
            if self.newEvt : 
                if self.idle:
                    ledDys388.clear()
                v =  self.animArr[self.index]
                print 'write color',self.index
                ledDys388.write(self.color, v)
                self.idle = False
                self.newEvt = False
                time.sleep(0.2)
                self.count+=1
            time.sleep(0.1)
    
    def smile(self):
        if self.idle:
            pass
        else:
            ledDys388.clear()
            ledDys388.write(ledDys388.colorG, ledicon.faceSmile)
            self.idle = True
    
    def setIndex(self,i):
        if i <  len(self.animArr):
            if  self.index != i:
                self.index = i
                self.newEvt = True
                
    def setColor(self,c):
        if c != self.color:
            ledDys388.clear()
            self.color = c
        
def init():
    ledDys388.init()

    
def _writeToLedArrow():
    global _lastWriteLed
    if _stdDevTotal > 199 :
        # find max'index in stddev3x3
        index3x3 = np.argmax(_stdDev3x3)
        # found index
        if index3x3 != _lastWriteLed:
            c = _stdDevTotal > 600 and ledDys388.colorR or ledDys388.colorB
            ledDys388.clear()
            ledDys388.write(c, ledicon.arrow3x3[index3x3])
        _lastWriteLed = index3x3
    else:
        if _lastWriteLed != 99:
            ledDys388.clear()
            ledDys388.write(ledDys388.colorG, ledicon.faceSmile)
        _lastWriteLed = 99


# ledAnim = AnimLed(ledicon.circleAnim4)
ledCircle = CircleLed(ledicon.circleAnim4)

def stop():
    ledCircle.stop()
    
def handleSizeLed(targetValue):
    if targetValue > 199 :       
        index = 0
        if targetValue < 500:
            index = 0
        elif targetValue < 800:
            index = 1
        elif targetValue < 1200:
            index = 2
        else:
            index = 3
        ledCircle.setIndex(index)
    else :
        ledCircle.smile()
    
def handleLedArrowColor(sizeTotalStd,std3x3):
    global _stdDevTotal,_stdDev3x3, _flagNewEvt
    _stdDevTotal = sizeTotalStd
    _stdDev3x3 = std3x3
    _flagNewEvt = True
    #print 'handleLedColor',_flagNewEvt,time.time()