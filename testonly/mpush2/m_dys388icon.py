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

def toRot90x4Value(raw):
    down = np.array(raw).reshape(8, 8)
    #print down
    right = np.rot90(down.copy())
    up = np.rot90(right.copy())
    left = np.rot90(up.copy())
    downArr =  [bits2Byte(down[i]) for i in range(8)]
    upArr =  [bits2Byte(up[i]) for i in range(8)]
    rightArr =  [bits2Byte(right[i]) for i in range(8)]
    leftArr =  [bits2Byte(left[i]) for i in range(8)]
    #print [bin(i) for i in upArr]
    return (downArr,rightArr,upArr, leftArr)

def toValueArr(raw):
    arr = np.array(raw).reshape(8, 8)
    return [bits2Byte(arr[i]) for i in range(8)]

arrowNoneBits = [ 
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    1,1,1,1,1,1,1,1
    ]

arrowCenterBits = [ 
    0,0,0,0,0,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,1,1,1,1,0,0,
    0,1,1,1,1,1,1,0,
    0,1,1,1,1,1,1,0,
    0,0,1,1,1,1,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,0,0,0,0,0
    ]

arrowDownBits = [ 
    0,0,0,1,1,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,1,1,0,0,0,
    1,1,1,1,1,1,1,1,
    0,1,1,1,1,1,1,0,
    0,0,1,1,1,1,0,0,
    0,0,0,1,1,0,0,0
    ]

arrowBottomRightBits = [ 
    0,1,0,0,0,0,0,0,
    1,1,1,0,0,0,0,0,
    0,1,1,1,0,0,0,0,
    0,0,1,1,1,0,0,1,
    0,0,0,1,1,1,1,1,
    0,0,0,0,1,1,1,1,
    0,0,0,0,1,1,1,1,
    0,0,0,1,1,1,1,1
    ]

def get3x3Arrow():
    durlArr1 = toRot90x4Value(arrowDownBits)
    durlArr2 = toRot90x4Value(arrowBottomRightBits)
    # 3x3 
    rarr = [None]*9
    rarr[7] = durlArr1[0]
    rarr[5] = durlArr1[1]
    rarr[1] = durlArr1[2]
    rarr[3] = durlArr1[3]
    
    rarr[4] = toValueArr(arrowCenterBits)

    rarr[8] = durlArr2[0]
    rarr[2] = durlArr2[1]
    rarr[0] = durlArr2[2]
    rarr[6] = durlArr2[3]
    return rarr

arrowNone = toValueArr(arrowNoneBits)
arrow3x3 = get3x3Arrow()

    
#x = toRot90x4Value(arrowDownData)
#print x[0]
