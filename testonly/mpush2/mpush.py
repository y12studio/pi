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
'''
python 2.7
pi@raspberrypi ~ $ echo $LANG
zh_TW.UTF-8

PIL fork
https://pypi.python.org/pypi/Pillow/2.2.1

Any io.UnsupportedOperation: fileno problem 
reinstall pillow again (sudo)

raspberry pi 
$ sudo pip uninstall PIL
$ sudo pip uninstall pillow
$ sudo pip install pillow

http://host:8888/
'''
import m_settings, m_pushover, m_tornado
import  m_led as led
import picamera
import logging, threading, io, struct
import datetime, time
from PIL import Image
import httplib, urllib, json
import collections, array
import numpy as np

# False when test
lastEvtTime = 0
width, height = 320, 240
stream = io.BytesIO()
temps = io.BytesIO()
queueLimit = 9
stdQueue = collections.deque(maxlen=queueLimit)
arrStdQueue = []
lastSize = 0
lastArrSize = []

def found(q):
    global lastEvtTime
    lastEvtTime = time.time()
    logging.info("EVENT FOUND")
    m_pushover.sendPushover(q)

def initLog():
    dateTag = datetime.datetime.now().strftime("%Y%b%d_%H%M%S")
    logging.basicConfig(filename="mpush2_%s.log" % dateTag, level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s : %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    logging.info('Started')

def handleMotion(k, q):
    if isMotion4(k):
        ediff = time.time() - lastEvtTime
        logging.debug("EvtTimeDiff=%d" % ediff)
        if ediff > 300:
            found(q)

#def testBinaryWrite():
#    return bytes(bytearray([0x13, 0x00, 0x00, 0x00, 0x08, 0x00]))

 
#def testWriteBinJpeg(st):
    #m_tornado.writeToWs('[1]')
    #m_tornado.writeToWs(st.getvalue(), binary=True)

def getPilJpgSize(im):
    im.save(temps, 'jpeg')
    size = temps.tell()
    temps.seek(0)
    return size

def pilCrop3x3(st, dim):
    global lastArrSize
    st.seek(0)
    base = Image.open(st)
    wx = int(width / dim)
    hy = int(height / dim)
    sarr = []
    result3x3 = []
    for yi in xrange(dim):
        for xi in xrange(dim):
            x, y = xi * wx, yi * hy
            # print x, y
            imcrop = base.crop((x, y, x + wx, y + hy))
            s = getPilJpgSize(imcrop)
            sarr.append(s)
            if len(lastArrSize) > 0 :
                index = yi*dim + xi
                #print index
                diff = abs(lastArrSize[index]-s)
                q = arrStdQueue[index]
                q.append(diff)
                stddev = int(np.std(q))
                result3x3.append(stddev)
    base.save(st, 'JPEG')
    lastArrSize = sarr
    return (st.getvalue(),result3x3)
        
def testWritePilWithThumbnailOver(st):
    st.seek(0)
    base = Image.open(st)
    tpil = base.copy()
    tpil.thumbnail((int(width / 2), int(height / 2)), Image.ANTIALIAS)
    base.paste(tpil.convert('L'), (10, 10))
    st.seek(0)
    base.save(st, 'JPEG')
    #m_tornado.writeToWs('[1]')
    #m_tornado.writeToWs(st.getvalue(), binary=True)

             
def runSizeDiffCheck():
    global lastSize
    with picamera.PiCamera() as camera:
         camera.resolution = (width, height)
         camera.framerate = 3
         camera.vflip = True
         time.sleep(2)
         start = time.time()
         count = 0
         led.init()
         # Use the video-port for captures...
         for foo in camera.capture_continuous(stream, 'jpeg',
                                             use_video_port=True):
             size = stream.tell()
             if lastSize > 0 :
                stdQueue.append(abs(size - lastSize))
                 # print stdQueue
                stddev = int(np.std(stdQueue))
                try:
                    img, std3x3 = pilCrop3x3(stream, 3)
                    m_tornado.writeToWs(img,stddev,std3x3)
                    led.handleLedColor(stddev,std3x3)
                except IOError:
                    pass
             lastSize = size
             count += 1
             stream.seek(0)
             #print('Size: %d /Captured %d images at %.2ffps' % (size, count, count / (time.time() - start)))

def main():
    initLog()
    for i in range(9):
        arrStdQueue.append(collections.deque(maxlen=queueLimit))
    t = threading.Thread(target=m_tornado.startTornado).start()
    try:
       runSizeDiffCheck()
    except (KeyboardInterrupt, SystemExit):
       m_tornado.stopTornado()
       led.stop()
       raise

if __name__ == '__main__':
    main()
