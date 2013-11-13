# coding=utf-8
'''
python 2.7
pi@raspberrypi ~ $ echo $LANG
zh_TW.UTF-8

https://pypi.python.org/pypi/Pillow/2.2.1
https://github.com/ashtons/picam

http://host:8888/
'''
import m_settings,m_pushover,m_tornado
import picam
import logging, threading,io,struct
import datetime, time
import Image
import httplib, urllib, json
import collections, array

# False when test
lastEvtTime = 0
width = 100
height = 100
stream = io.BytesIO()

def found(q):
    global lastEvtTime
    lastEvtTime = time.time()
    logging.info("EVENT FOUND")
    m_pushover.sendPushover(q)

def initLog():
    dateTag = datetime.datetime.now().strftime("%Y%b%d_%H%M%S")
    logging.basicConfig(filename="mt_%s.log" % dateTag, level=logging.DEBUG,
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
    t = threading.Thread(target=m_tornado.startTornado).start()
    try:
       runDiffCheck()
    except (KeyboardInterrupt, SystemExit):
       m_tornado.stopTornado()
       raise

def testBinaryWrite():
    return bytes(bytearray([0x13, 0x00, 0x00, 0x00, 0x08, 0x00]))

 
def testWriteBinJpeg():
    if m_tornado.WSHandler.wsClients() > 0:
        img = picam.takePhotoWithDetails(width,height, 85)
        img.save(stream,'JPEG', quality=70)
        m_tornado.WSHandler.wsSend('[5]')
        m_tornado.WSHandler.wsSend(stream.getvalue(),binary=True)
        stream.seek(0)

def testWriteBinRgb(rgbIntList):
    if m_tornado.WSHandler.wsClients() > 0:
        m_tornado.WSHandler.wsSend('[6]')
        bytearr = bytearray()
        for rgb in rgbIntList:
            rarr = [ ord(c) for c in struct.pack("I", rgb) ]
            # return [R,G,B,0]
            bytearr.append(rarr[0])
            bytearr.append(rarr[1])
            bytearr.append(rarr[2])
        m_tornado.WSHandler.wsSend(bytes(bytearr),binary=True)
        
def runDiffCheck():
    k = collections.deque(maxlen=4)
    THRESHOLD = 15
    QUANITY_MIN = 50
   
    f1 = picam.takeRGBPhotoWithDetails(width, height)
   
    while True:
        f2 = picam.takeRGBPhotoWithDetails(width, height)
        m_tornado.WSHandler.wsSend(json.dumps(f2))
        (m, q) = picam.difference(f1, f2, THRESHOLD)
        testWriteBinRgb(m)
        if q > 10 : logging.debug("px=%d", q)
        k.append(q)
        # print 'px %d' %q
        msg = []
        msg.append(q)
        msg.append(m)
        m_tornado.WSHandler.wsSend(json.dumps(msg))
        testWriteBinJpeg()
        picam.LEDOn() if q > QUANITY_MIN  else  picam.LEDOff()
        handleMotion(k, q)
        f1 = f2

if __name__ == '__main__':
    main()
