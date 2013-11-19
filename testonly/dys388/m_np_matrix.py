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
import numpy as np

def bits2Byte(x):
    r = 0
    for i in range(8):
        v = x[7-i]
        r += (2**i*v)
    return r

def toDownUpRL(raw):
    down = np.array(raw).reshape(8, 8)
    #print down
    up = np.flipud(down.copy())
    right = np.rot90(down.copy())
    left = np.fliplr(right.copy())
    downArr =  [bits2Byte(down[i]) for i in range(8)]
    upArr =  [bits2Byte(up[i]) for i in range(8)]
    rightArr =  [bits2Byte(right[i]) for i in range(8)]
    leftArr =  [bits2Byte(left[i]) for i in range(8)]
    #print [bin(i) for i in upArr]
    return (downArr,upArr,rightArr,leftArr)
    
#x = toDownUpRL(arrowDownData)
#print x[0]
