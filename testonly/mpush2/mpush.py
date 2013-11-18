# coding=utf-8
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
stdQueue = collections.deque(maxlen=10)
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

def isMotion4(kl):
    return len(kl) == 4 and kl[1] - kl[0] > 777 and kl[2] > 1000 and kl[3] > 1000

def handleMotion(k, q):
    if isMotion4(k):
        ediff = time.time() - lastEvtTime
        logging.debug("EvtTimeDiff=%d" % ediff)
        if ediff > 300:
            found(q)

def main():
    initLog()
    for i in range(9):
        arrStdQueue.append(collections.deque(maxlen=10))
    t = threading.Thread(target=m_tornado.startTornado).start()
    try:
       runDiffCheck()
    except (KeyboardInterrupt, SystemExit):
       m_tornado.stopTornado()
       raise

def testBinaryWrite():
    return bytes(bytearray([0x13, 0x00, 0x00, 0x00, 0x08, 0x00]))

 
def testWriteBinJpeg(st):
    if m_tornado.WSHandler.wsClients() > 0:       
        m_tornado.WSHandler.wsSend('[1]')
        m_tornado.WSHandler.wsSend(st.getvalue(), binary=True)

def getPilJpgSize(im):
    im.save(temps, 'jpeg')
    size = temps.tell()
    temps.seek(0)
    return size

def testWritePilCrop(st, dim):
    global lastArrSize
    st.seek(0)
    base = Image.open(st)
    wx = int(width / dim)
    hy = int(height / dim)
    sarr = []
    result = []
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
                result.append(stddev)
    if len(result) > 0:
        jr = []
        jr.append(3)
        jr.append(result)
        m_tornado.WSHandler.wsSend(json.dumps(jr))
    base.save(st, 'JPEG')
    m_tornado.WSHandler.wsSend('[1]')
    m_tornado.WSHandler.wsSend(st.getvalue(), binary=True)
    lastArrSize = sarr
        
def testWritePilWithThumbnailOver(st):
    st.seek(0)
    base = Image.open(st)
    tpil = base.copy()
    tpil.thumbnail((int(width / 2), int(height / 2)), Image.ANTIALIAS)
    base.paste(tpil.convert('L'), (10, 10))
    st.seek(0)
    base.save(st, 'JPEG')
    m_tornado.WSHandler.wsSend('[1]')
    m_tornado.WSHandler.wsSend(st.getvalue(), binary=True)
        
def testWritePil(st):
    st.seek(0)
    base = Image.open(st)
    st.seek(0)
    base.save(st, 'JPEG')
    m_tornado.WSHandler.wsSend('[1]')
    m_tornado.WSHandler.wsSend(st.getvalue(), binary=True)
                
def runDiffCheck():
    global lastSize
    with picamera.PiCamera() as camera:
         camera.resolution = (width, height)
         camera.framerate = 3
         camera.vflip = True
         time.sleep(2)
         start = time.time()
         count = 0
         # Use the video-port for captures...
         for foo in camera.capture_continuous(stream, 'jpeg',
                                             use_video_port=True):
             size = stream.tell()
             if lastSize > 0 :
                 stdQueue.append(abs(size - lastSize))
                 # print stdQueue
                 stddev = int(np.std(stdQueue))
                 m_tornado.WSHandler.wsSend('[2,%d]' % stddev)
             lastSize = size
             testWritePilCrop(stream, 3)
             #testWritePil(stream)
             # testWriteBinJpeg(stream)
             count += 1
             stream.seek(0)
             #print('Size: %d /Captured %d images at %.2ffps' % (size, count, count / (time.time() - start)))

if __name__ == '__main__':
    main()
