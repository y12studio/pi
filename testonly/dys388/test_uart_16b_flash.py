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
import serial, time, struct, random

def toByte(s):
    return chr(int(s, 2))

# for USB_serial_line
# port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=3.0)
port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)

byte1Clear16 = toByte('10000000')
byte1Show16 = toByte('00000000')

rowArrShow = [ 
              1, 1, 0, 1, 0, 0, 0, 0,
              0, 0, 1, 0, 0, 0, 0, 0,
              0, 0, 1, 0, 0, 0, 0, 0,
              0, 0, 1, 0, 0, 0, 0, 1,
              0, 0, 1, 0, 0, 0, 0, 1,
              0, 0, 1, 0, 0, 0, 0, 0,
              0, 0, 1, 0, 0, 0, 0, 0,
              0, 1, 0, 1, 0, 0, 0, 1,
              ]
rowArrR = [ 
              0, 31, 0, 31, 0, 0, 0, 0,
              0, 0, 31, 0, 0, 0, 0, 0,
              0, 0, 31, 0, 0, 0, 0, 0,
              0, 0, 1, 0, 0, 0, 0, 0,
              0, 0, 1, 0, 0, 0, 0, 0,
              0, 0, 1, 0, 0, 0, 0, 0,
              0, 0, 31, 0, 0, 0, 0, 0,
              0, 31, 0, 31, 0, 0, 0, 0,
              ]
rowArrG = [ 
              0, 3, 0, 3, 0, 0, 0, 0,
              0, 0, 3, 0, 0, 0, 0, 0,
              0, 0, 31, 0, 0, 0, 0, 0,
              0, 0, 31, 0, 0, 0, 0, 0,
              0, 0, 31, 0, 0, 0, 0, 0,
              0, 0, 31, 0, 0, 0, 0, 0,
              0, 0, 3, 0, 0, 0, 0, 0,
              0, 3, 0, 3, 0, 0, 0, 0,
              ]

rowArrB = [ 
              0, 1, 0, 1, 0, 0, 0, 0,
              0, 0, 1, 0, 0, 0, 0, 0,
              0, 0, 1, 0, 0, 0, 0, 0,
              0, 0, 1, 0, 0, 0, 0, 31,
              0, 0, 1, 0, 0, 0, 0, 31,
              0, 0, 1, 0, 0, 0, 0, 0,
              0, 0, 1, 0, 0, 0, 0, 0,
              0, 1, 0, 1, 0, 0, 0, 0,
              ]



def calcColor():
    r = []
    for i in range(64):
        # (R<<10) + (G<<5) +B)
        rgb = (rowArrR[i] << 10) + (rowArrG[i] << 5) + rowArrB[i]
        v = rgb * rowArrShow[i]
        r.append((v >> 8) & 0xff)
        r.append(v & 0xff)
    return r

def changeColor(c):
       rowArrR[0] = random.randint(0, 31)
       rowArrG[0] = random.randint(0, 31)
       rowArrB[0] = random.randint(0, 31)
       rowArrR[63] = random.randint(0, 31)
       rowArrG[63] = random.randint(0, 31)
       rowArrB[63] = random.randint(0, 31)
    # print rowArrR[63], rowArrG[63], rowArrB[63]
        
count = 0

while True:
    count += 1
    port.write(byte1Clear16)
    # sleep less1600ms
    time.sleep(2)
    changeColor(count)
    r = calcColor()
    port.write(byte1Show16)
    for i in r:
        # print i
        port.write(chr(i))
    time.sleep(5)
