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

# brightness 0-31
brightness = 16
delay = 0.001 / 1000.0
clearData = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
addrData = 0x01
colorClear =(31 << 1) | 0x07
colorR = (brightness << 3) + 4
colorG = (brightness << 3) + 2
colorB = (brightness << 3) + 1

def init():
    GPIO.setwarnings(False)
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
    clear()
    
def clear():
    DbpWrite(addrData,colorClear,clearData)

def write(color,data):
    clear()
    DbpWrite(addrData,color,data)
    
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
