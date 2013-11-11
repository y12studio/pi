# coding=utf-8
'''
pi@raspberrypi ~ $ echo $LANG
zh_TW.UTF-8
https://github.com/ashtons/picam

url http://host:port/s/foo_webapp.html 
'''
import settings
import picam
import logging,threading
import datetime,time
import Image
import httplib, urllib
import collections,array
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

# False when test
lastEvtTime = 0

class WSHandler(tornado.websocket.WebSocketHandler):
  connections = set()
  lock = threading.Lock()
  def open(self):
      print 'New connection was opened'
      #self.write_message("Welcome to my websocket!")
      self.lock.acquire()
      try:
          self.connections.add(self)
      finally:
          self.lock.release()

  def on_message(self, message):
      print 'Incoming message:', message
      #self.write_message("You said: " + message)

  def on_close(self):
      print 'Connection was closed...'
      self.lock.acquire()
      try:
          self.connections.remove(self)
      finally:
          self.lock.release()


  @classmethod
  def wsSend(cls,msg):
      #logging.debug("sending message %s" %msg)
      cls.lock.acquire()
      try:
          for conn in cls.connections:
              try:
                  conn.write_message(msg)
              except:
                  logging.error("Error sending message",exc_info=True)
      finally:
          cls.lock.release()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello Test")

application = tornado.web.Application([
  (r'/ws', WSHandler),(r'/',MainHandler),
  (r'/s/(.*)', tornado.web.StaticFileHandler, {'path': settings.WWW}),
])

def pushoverPost(msg):
    if not settings.PUSHOVER_ENABLE :
       logging.info('[TestPrintOnly]Send pushover event')
       return
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.urlencode({
          "token": settings.PUSHOVER_APPTOKEN,
          "user": settings.PUSHOVER_USERKEY,
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
    t = threading.Thread(target=pushoverPost, args=(m,))
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

def startTornado():
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(settings.PORT)
    tornado.ioloop.IOLoop.instance().start()

def stopTornado():
    tornado.ioloop.IOLoop.instance().stop()

def main():
    initLog()
    t = threading.Thread(target=startTornado).start()
    try:
       runDiffCheck()
    except (KeyboardInterrupt, SystemExit):
       stopTornado()
       raise

def runDiffCheck():
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
        #print 'px %d' %q
        WSHandler.wsSend(str(q))
        picam.LEDOn() if q > QUANITY_MIN  else  picam.LEDOff()
        handleMotion(k,q)
        f1 = f2

if __name__ == '__main__':
    main()
