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
import collections, array
import numpy as np
from scipy import stats

class StatSizeDiff:
    def __init__(self, queueSize):
        self.size = queueSize
        self.xi = np.arange(0,queueSize)
        self.sizeQueue = collections.deque(maxlen=queueSize)
        self.diffQueue = collections.deque(maxlen=queueSize)
        self.stdQueue = collections.deque(maxlen=queueSize)
        self.rQueue = collections.deque(maxlen=queueSize)
        for i in range(queueSize):
            self.sizeQueue.append(0)
            self.diffQueue.append(0)
            self.stdQueue.append(0)
            self.rQueue.append(0)
        
    def getNpStd(self,s):
        self._addSize(s)
        stddev = int(np.std(self.diffQueue))
        self.stdQueue.append(stddev)
        #print 'STD_DEV=',['%.2f'%i for i in self.stdQueue]
        return stddev
        
    def _addSize(self,s):
        self.sizeQueue.append(s)
        #print "SIZE=",self.sizeQueue
        diff = abs(self.sizeQueue[self.size-1]-self.sizeQueue[self.size-2])
        self.diffQueue.append(diff)
        #print "DIFF=",self.diffQueue        
            
    def getScipiLinregress(self,s):
        self._addSize(s)
        slope, intercept, r_value, p_value, std_err = stats.linregress(self.xi,self.diffQueue)
        self.stdQueue.append(std_err)
        self.rQueue.append(r_value)
        #print 'STDERR=',['%.2f'%i for i in self.stdQueue]
        #print 'R=',['%.2f'%i for i in self.rQueue]
        return std_err
        
