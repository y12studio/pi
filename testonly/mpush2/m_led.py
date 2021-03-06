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
import m_thread as mt

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

class LedCircleWorker(mt.BaseWorker):
    def __init__(self):
        mt.BaseWorker.__init__(self)
        self.animArr = ledicon.circleAnim4
        self.color = ledDys388.colorR
        #self.ledCircle = CircleLed(ledicon.circleAnim4)
        self.lastSmile = False
    
    def initLed(self):
        ledDys388.init()
                
    def handleEvent(self):
        targetValue = self.data
        #print 'EVT Value=',targetValue
        if targetValue > 66 :       
            index = 0
            if targetValue < 300:
                index = 0
            elif targetValue < 600:
                index = 1
            elif targetValue < 1000:
                index = 2
            else:
                index = 3
            icon =  self.animArr[index]
            if self.lastSmile:
                ledDys388.clear()
            ledDys388.write(self.color, icon)
            self.lastSmile = False
        else :
            if not self.lastSmile:
                ledDys388.clear()
                ledDys388.write(ledDys388.colorG, ledicon.faceSmile)
                self.lastSmile = True
        return