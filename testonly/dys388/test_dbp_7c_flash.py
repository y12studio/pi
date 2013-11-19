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
import time
import RPi.GPIO as GPIO
import m_np_matrix


def toByte(s):
    return chr(int(s, 2))

delay = 0.001 / 1000.0

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

durlArr = m_np_matrix.toDownUpRL(arrowDownBits)

clearData = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
addrData = 0x01
colorClear =(31 << 1) | 0x07
colorR = int('11111100',2)
colorG = int('11111010',2)
colorB = int('11111001',2)
colors = [colorR,colorG,colorB]
count = 0

def init():
    # Set the numbering sequence of the pins, then set pins ten and twelve to output, and pin eight to input. 
    # http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/turing-machine/two.html
    GPIO.setmode(GPIO.BOARD)
    # GPIO3  SDA 
    GPIO.setup(3, GPIO.OUT)
    # GPIO5 SCL
    GPIO.setup(5, GPIO.OUT)
    # GPIO7 INT/DBP
    GPIO.setup(7, GPIO.OUT)
    GPIO.output(3, True)
    GPIO.output(5, True)
    GPIO.output(7, True)

def DbpWriteByte(byteData):
    for i in range(8):
        if((byteData << i) & 0x80):
            GPIO.output(3, True)
        else:
             GPIO.output(3, False)
        GPIO.output(5, False)
        # 1ms
        time.sleep(delay)
        GPIO.output(5, True)

def DbpWrite(addr,color,data):
    time.sleep(1.0 / 1000.0)
    GPIO.output(7, False)
    time.sleep(delay)
    DbpWriteByte(addr)
    DbpWriteByte(color)
    for i in range(8):
         DbpWriteByte(data[i])
    GPIO.output(7, True)
    
init()

DbpWrite(addrData,colorClear,clearData)

while True:
    count+=1
    print time.time()
    DbpWrite(addrData,colors[count%len(colors)],durlArr[count%4])
    time.sleep(0.5)
    DbpWrite(addrData,colorClear,clearData)
    time.sleep(0.01)
