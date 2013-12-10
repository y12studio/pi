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
import m_settings, m_tornado, m_led, m_stat
import picamera
import logging, threading, io, struct
import datetime, time
from PIL import Image
import httplib, urllib, json
import collections, array
import numpy as np
from scipy import stats


# False when test
lastEvtTime = 0
width, height = 320, 240
fps = 5
stream = io.BytesIO()
temps = io.BytesIO()
# collections for 2 secs
queueLimit = fps * 2
statsHandlerTotal = m_stat.StatSizeDiff(queueLimit)
statsHandlerLeft = m_stat.StatSizeDiff(queueLimit)
statsHandlerRight = m_stat.StatSizeDiff(queueLimit)

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

def getPilJpgSize(im):
    im.save(temps, 'jpeg')
    size = temps.tell()
    temps.seek(0)
    return size

def cropLeftRight(st):
    ydim = 1;
    xdim = 2;
    wx = int(width / xdim)
    hy = int(height / ydim)
    st.seek(0)
    base = Image.open(st)
    sarr = []
    for yi in xrange(ydim):
        for xi in xrange(xdim):
            x, y = xi * wx, yi * hy
            # print x, y
            imcrop = base.crop((x, y, x + wx, y + hy))
            s = getPilJpgSize(imcrop)
            sarr.append(s)
    jpg = st.getvalue()
    return (jpg, sarr)

def cropLeftRightFake(st):
    st.seek(0)
    base = Image.open(st)
    sarr = []
    sarr.append(0)
    sarr.append(0)
    return (st.getvalue(), sarr)

def handleImgStream(asize, astream):
    try:
        stdDevTotal = statsHandlerTotal.addNpSize(asize)
        #jpg,stdDevArr = cropLeftRight(astream)
        jpg,stdDevArr = cropLeftRightFake(astream)
        stdDevLeft = statsHandlerLeft.addNpSize(stdDevArr[0])
        stdDevRight = statsHandlerRight.addNpSize(stdDevArr[1])
        #print "STDDEV,Total,L,R=",stdDevTotal, stdDevLeft,stdDevRight
        ledWorker.sendData(stdDevTotal)
        tornadoWorker.sendData((stdDevTotal,stdDevLeft,stdDevRight,jpg))
    except Exception as e:
        print "Exception:", e
             
ledWorker = m_led.LedCircleWorker()
tornadoWorker = m_tornado.TornadoHandlerHalfWorker()

def cameraCapture():
    with picamera.PiCamera() as camera:
         camera.resolution = (width, height)
         camera.framerate = fps
         camera.vflip = True
         time.sleep(2)
         start = time.time()
         count = 0
         ledWorker.initLed()
         # Use the video-port for captures...
         for foo in camera.capture_continuous(stream, 'jpeg',
                                             use_video_port=True):
             size = stream.tell()
             handleImgStream(size, stream)
             count += 1
             stream.seek(0)
             # print('Size: %d /Captured %d images at %.2ffps' % (size, count, count / (time.time() - start)))

def main():
    initLog()
    m_tornado.startTornado(m_settings.WWW, m_settings.PORT)
    try:
       cameraCapture()
    except (KeyboardInterrupt, SystemExit):
       m_tornado.stopTornado()
       ledWorker.stop()
       tornadoWorker.stop()
       raise

if __name__ == '__main__':
    main()
