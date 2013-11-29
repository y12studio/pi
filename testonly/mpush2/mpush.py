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
from scipy import stats
import m_stat as mstat


# False when test
lastEvtTime = 0
width, height = 320, 240
fps = 6
stream = io.BytesIO()
temps = io.BytesIO()
# collections for 2 secs
queueLimit = fps*2
diffQueue = collections.deque(maxlen=queueLimit)
stddevQueue = collections.deque(maxlen=queueLimit)
rQueue = collections.deque(maxlen=queueLimit)
xi = np.arange(0,queueLimit)
arrStdQueue = []
lastArrSize = []
statsHandler = mstat.StatSizeDiff(queueLimit)


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


def handleImgSizeOnly(asize,astream):
    try:
        stdDev = statsHandler.getNpStd(asize)
        #print "STD=",stdDev
        ledController.sendData(stdDev)
        jpg = astream.getvalue()
        tornadoController.sendData((stdDev,jpg))
    except Exception as e:
        print "Exception:",e
             
def runCameraInput():
    with picamera.PiCamera() as camera:
         camera.resolution = (width, height)
         camera.framerate = fps
         camera.vflip = True
         time.sleep(2)
         start = time.time()
         count = 0
         initLed()
         # Use the video-port for captures...
         for foo in camera.capture_continuous(stream, 'jpeg',
                                             use_video_port=True):
             size = stream.tell()
             #handleImgByCrop3x3AndArrow(size,stream)
             handleImgSizeOnly(size,stream)
             count += 1
             stream.seek(0)
             #print('Size: %d /Captured %d images at %.2ffps' % (size, count, count / (time.time() - start)))

ledController = None
tornadoController = None

def initLed():
    global ledController
    ledController = led.LedCircle()

def initTornado():
    global tornadoController
    tornadoController = m_tornado.TornadoHandlerSizeOnly()
    threading.Thread(target=m_tornado.startTornado).start()
     
def init3x3():
    '''
    FPS<=3 ONLY
    '''
    for i in range(9):
        arrStdQueue.append(collections.deque(maxlen=queueLimit))    



def main():
    initLog()
    initTornado()
    
    try:
       runCameraInput()
    except (KeyboardInterrupt, SystemExit):
       m_tornado.stopTornado()
       ledController.stop()
       raise

if __name__ == '__main__':
    main()
