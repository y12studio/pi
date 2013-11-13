# coding=utf-8
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
        <html><body><h2>The live Page <a href="/s/foo_webapp.html">Link</a></h2></body></html>
        """)

application = tornado.web.Application([
  (r'/ws', WSHandler), (r'/', MainHandler),
  (r'/s/(.*)', tornado.web.StaticFileHandler, {'path': m_settings.WWW}),
])

def startTornado():
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(m_settings.PORT)
    tornado.ioloop.IOLoop.instance().start()

def stopTornado():
    tornado.ioloop.IOLoop.instance().stop()