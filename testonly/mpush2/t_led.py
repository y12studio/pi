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
import m_led as led

ledDys388.init()

def testBrightChange():
    count = 0
    while True:
        brightness = (count % 16) * 2
        # green
        color = (brightness << 3) + 2
        ledDys388.write(color, ledicon.faceSmile)
        time.sleep(1)
        count+=1

x = led.AnimLed(ledicon.circleAnim4)
x.anim()
time.sleep(5)
x.setColor(ledDys388.colorG)
time.sleep(5)
x.setColor(ledDys388.colorB)
time.sleep(5)
x.stop()

