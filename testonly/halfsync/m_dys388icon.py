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

def toRot90x4NpArray(rawBit):
    down = np.array(rawBit).reshape(8, 8)
    right = np.rot90(down.copy())
    up = np.rot90(right.copy())
    left = np.rot90(up.copy())
    return (down,right,up, left)

def toRot90x4LedValue(rawBitArr):
    down = rawBitArr[0]
    #print down
    right = rawBitArr[1]
    up = rawBitArr[2]
    left = rawBitArr[3]
    downArr =  [bits2Byte(down[i]) for i in range(8)]
    upArr =  [bits2Byte(up[i]) for i in range(8)]
    rightArr =  [bits2Byte(right[i]) for i in range(8)]
    leftArr =  [bits2Byte(left[i]) for i in range(8)]
    #print [bin(i) for i in upArr]
    return (downArr,rightArr,upArr, leftArr)

def _getAnimArrow(raw,shift,axis):
    r = []
    r.append(toValueArr(raw))
    a = np.array(raw).reshape(8, 8)
    for i in range(7):
        v = np.roll(a.copy(),(i+1)*shift,axis=axis)
        #print v
        r.append([bits2Byte(v[j]) for j in range(8)])
    return r

def toValueArr(rawBit):
    arr = np.array(rawBit).reshape(8, 8)
    return [bits2Byte(arr[i]) for i in range(8)]


_iconSad = [ 
    0,0,0,0,0,0,0,0,
    0,0,1,0,0,1,0,0,
    0,1,1,0,0,1,1,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,1,1,1,1,1,1,0,
    1,0,0,0,0,0,0,1
    ]

_iconSmile = [ 
    0,0,0,0,0,0,0,0,
    0,1,1,0,0,1,1,0,
    0,0,1,0,0,1,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    1,0,0,0,0,0,0,1,
    0,1,1,1,1,1,1,0,
    0,0,0,0,0,0,0,0
    ]

circleBits1 = [ 
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0
    ]

circleBits2 = [ 
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,1,1,1,1,0,0,
    0,0,1,1,1,1,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0
    ]

circleBits3 = [ 
    0,0,0,0,0,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,1,1,1,1,0,0,
    0,1,1,1,1,1,1,0,
    0,1,1,1,1,1,1,0,
    0,0,1,1,1,1,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,0,0,0,0,0
    ]

circleBits4 = [ 
    0,0,0,1,1,0,0,0,
    0,0,1,1,1,1,0,0,
    0,1,1,1,1,1,1,0,
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,
    0,1,1,1,1,1,1,0,
    0,0,1,1,1,1,0,0,
    0,0,0,1,1,0,0,0
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
    0,0,0,0,0,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,1,1,0,0,0,
    1,1,1,1,1,1,1,1,
    0,1,1,1,1,1,1,0,
    0,0,1,1,1,1,0,0,
    0,0,0,1,1,0,0,0
    ]

arrowBottomRightBits = [ 
    0,0,0,0,0,0,0,0,
    0,0,1,0,0,0,0,0,
    0,1,1,1,0,0,0,0,
    0,0,1,1,1,0,0,1,
    0,0,0,1,1,1,1,1,
    0,0,0,0,1,1,1,1,
    0,0,0,0,1,1,1,1,
    0,0,0,1,1,1,1,1
    ]

arrowNpArrDRUL = toRot90x4NpArray(arrowDownBits)
arrowNpArrDRUL2 = toRot90x4NpArray(arrowBottomRightBits)

def _get3x3Arrow():
    arr1 = toRot90x4LedValue(arrowNpArrDRUL)
    arr2 = toRot90x4LedValue(arrowNpArrDRUL2)
    # 3x3 
    rarr = [None]*9
    rarr[7] = arr1[0]
    rarr[5] = arr1[1]
    rarr[1] = arr1[2]
    rarr[3] = arr1[3]
    
    rarr[4] = toValueArr(arrowCenterBits)

    rarr[8] = arr2[0]
    rarr[2] = arr2[1]
    rarr[0] = arr2[2]
    rarr[6] = arr2[3]
    return rarr

arrow3x3 = _get3x3Arrow()
faceSad = toValueArr(_iconSad)
faceSmile = toValueArr(_iconSmile)
upArrow8 =  _getAnimArrow(arrowNpArrDRUL[2],-1,0)
downArrow8 =  _getAnimArrow(arrowNpArrDRUL[0],1,0)
rightArrow8 =  _getAnimArrow(arrowNpArrDRUL[1],1,1)
leftArrow8 =  _getAnimArrow(arrowNpArrDRUL[3],-1,1)
circleAnim4 = [toValueArr(i) for i in [circleBits1,circleBits2,circleBits3,circleBits4]]




#x = toRot90x4LedValue(arrowDownData)
#print x[0]
