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

def init():
    ledDys388.init()
    t = threading.Thread(target=writefunc, args=(0,))
    t.start()

def writefunc(i):
    global _flagNewEvt
    while _flagRun:
        #print 'InThread ',_flagNewEvt,time.time()
        if _flagNewEvt :
            _writeToLed()
            _flagNewEvt = False
        else :
            time.sleep(0.1)

def stop():
    global _flagRun
    _flagRun = False
    
def _writeToLed():
    global _lastWriteLed
    if _stdDevTotal > 199 :
        # find max'index in stddev3x3
        index3x3 = np.argmax(_stdDev3x3)
        # found index
        if index3x3 != _lastWriteLed:
            c = _stdDevTotal > 600 and ledDys388.colorR or ledDys388.colorB
            ledDys388.write(c, ledicon.arrow3x3[index3x3])
        _lastWriteLed = index3x3
    else:
        if _lastWriteLed != 99:
            ledDys388.write(ledDys388.colorG, ledicon.arrowNone)
        _lastWriteLed = 99

def handleLedColor(sizeTotalStd,std3x3):
    global _stdDevTotal,_stdDev3x3, _flagNewEvt
    _stdDevTotal = sizeTotalStd
    _stdDev3x3 = std3x3
    _flagNewEvt = True
    #print 'handleLedColor',_flagNewEvt,time.time()