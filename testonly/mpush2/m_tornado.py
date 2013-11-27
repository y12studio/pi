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
TODO
'''
import m_settings
import logging, threading
import datetime, time
import httplib, urllib, json
import collections, array
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

class WSHandler(tornado.websocket.WebSocketHandler):
  connections = set()
  lock = threading.Lock()
  def open(self):
      print 'New connection was opened'
      # self.write_message("Welcome to my websocket!")
      self.lock.acquire()
      try:
          self.connections.add(self)
      finally:
          self.lock.release()

  def on_message(self, message):
      print 'Incoming message:', message
      # self.write_message("You said: " + message)

  def on_close(self):
      print 'Connection was closed...'
      self.lock.acquire()
      try:
          self.connections.remove(self)
      finally:
          self.lock.release()

  @classmethod
  def wsClients(cls):
      r = 0
      # logging.debug("sending message %s" %msg)
      cls.lock.acquire()
      try:
          r = len(cls.connections)
      finally:
          cls.lock.release()
      return r


  @classmethod
  def wsSend(cls, msg, binary=False):
      # logging.debug("sending message %s" %msg)
      cls.lock.acquire()
      try:
          for conn in cls.connections:
              try:
                  conn.write_message(msg, binary)
              except:
                  logging.error("Error sending message", exc_info=True)
      finally:
          cls.lock.release()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("""
        <html><body><h1>TEST Page <a href="/s/mpush2.html">Link</a>.</h1></body></html>
        """)

application = tornado.web.Application([
  (r'/ws', WSHandler), (r'/', MainHandler),
  (r'/s/(.*)', tornado.web.StaticFileHandler, {'path': m_settings.WWW}),
])

def startTornado():
    t = threading.Thread(target=worker, args=(0,))
    t.start()
    
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(m_settings.PORT)
    tornado.ioloop.IOLoop.instance().start()
    
_img = None
_stdTotal = None
_std3x3 = None
_flagNewEvt = -1
_flagRun = True

def worker(i):
    global _flagNewEvt
    while _flagRun:
        #print 'Worker',_flagNewEvt,time.time()
        if _flagNewEvt > 0 :
            _writeToWsStd3x3(_flagNewEvt==2)
            _flagNewEvt = -1
        else :
            time.sleep(0.1)

def _writeToWsStd3x3(imgEnable):
    WSHandler.wsSend('[2,%d]' % _stdTotal)
    if imgEnable:
        WSHandler.wsSend('[1]')
        WSHandler.wsSend(_img, binary=True)
    if len(_std3x3) > 0:
        jr = []
        jr.append(3)
        jr.append(_std3x3)
        WSHandler.wsSend(json.dumps(jr))

def writeToWsStd3x3(img, stdTotal, std3x3):
    global _img,_stdTotal,_std3x3,_flagNewEvt
    _stdTotal = stdTotal
    _std3x3 = std3x3
    if stdTotal > 100:
        _img = img
        # 2 img
        _flagNewEvt = 2
    else:
        # 1 for non-img
        _flagNewEvt = 1
    #print 'writeToWs',_flagNewEvt,time.time()

def stopTornado():
    global _flagRun
    _flagRun = False
    tornado.ioloop.IOLoop.instance().stop()