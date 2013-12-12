# coding=utf-8
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
import io
import time
import picamera
import cv2
import numpy as np

def getCvImg():
    # Create the in-memory stream
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(2)
        camera.capture(stream, format='jpeg')
        # Construct a numpy array from the stream
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        # "Decode" the image from the array, preserving colour
        img = cv2.imdecode(data, 1)
    return img
    
img = getCvImg()
# [B,G,R]
px = img[100,100]
print px
# accessing only blue pixel
blue = img[100,100,0]
print blue

# accessing RED value
print img.item(10,10,2)

# modifying RED value
img.itemset((10,10,2),100)
print img.item(10,10,2)
# 480x640 h,w,channels
print 'img.shape',img.shape