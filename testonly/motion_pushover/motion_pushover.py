# coding=utf-8
'''
pi@raspberrypi ~ $ echo $LANG
zh_TW.UTF-8
check https://github.com/ashtons/picam
'''
import picam
import logging
import datetime
from PIL import Image
from array import array
import time
from threading import Thread
import httplib, urllib
import collections
# False when test
PUSHOVER_ENABLE = True
PUSHOVER_APPTOKEN="xx"
PUSHOVER_USERKEY="xx"
lastEvtTime = 0

def pushoverPost(msg):
    if not PUSHOVER_ENABLE :
       logging.info('[TestPrintOnly]Send pushover event')
       return
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.urlencode({
          "token": PUSHOVER_APPTOKEN,
          "user": PUSHOVER_USERKEY,
          "message": msg,
         }), { "Content-type": "application/x-www-form-urlencoded" })
    logging.info('HTTP POST Send %s' % msg)
    r = conn.getresponse()
    logging.info("HTTP POST status=%d , reason=%s",r.status,r.reason)
    logging.info(r.read())
    conn.close()

def found(q):
    global lastEvtTime
    lastEvtTime = time.time()
    logging.info("EVENT FOUND")
    m =  '我家F門 Event px=%d'%q
    t = Thread(target=pushoverPost, args=(m,))
    t.start()

def initLog():
    dateTag = datetime.datetime.now().strftime("%Y%b%d_%H%M%S")
    logging.basicConfig(filename="mt_%s.log"%dateTag,level=logging.DEBUG,
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
    return len(kl)==4 and kl[1]-kl[0] > 777 and kl[2] > 1000 and kl[3] > 1000

def handleMotion(k,q):
    if isMotion4(k):
        ediff = time.time() - lastEvtTime
        logging.debug("EvtTimeDiff=%d" % ediff)
        if ediff > 300:
            found(q)

def main():
    initLog()
    k = collections.deque(maxlen=4)
    width = 100
    height = 100
    THRESHOLD = 15
    QUANITY_MIN = 50

    f1 = picam.takeRGBPhotoWithDetails(width,height)

    while True:
        f2 = picam.takeRGBPhotoWithDetails(width,height)
        (_,q) = picam.difference(f1,f2,THRESHOLD)
        if q > 10 : logging.debug("px=%d", q)
        k.append(q)
        picam.LEDOn() if q > QUANITY_MIN  else  picam.LEDOff()
        handleMotion(k,q)
        f1 = f2

if __name__ == '__main__':
    main()
