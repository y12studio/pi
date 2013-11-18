# coding=utf-8
'''
pi@raspberrypi ~ $ echo $LANG
zh_TW.UTF-8
'''
import m_settings
import logging, threading
import datetime, time
import httplib, urllib, json
import collections, array

def pushoverPost(msg):
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.urlencode({
          "token": m_settings.PUSHOVER_APPTOKEN,
          "user": m_settings.PUSHOVER_USERKEY,
          "message": msg,
         }), { "Content-type": "application/x-www-form-urlencoded" })
    logging.info('HTTP POST Send %s' % msg)
    r = conn.getresponse()
    logging.info("HTTP POST status=%d , reason=%s", r.status, r.reason)
    logging.info(r.read())
    conn.close()

def sendPushover(q):
    if not m_settings.PUSHOVER_ENABLE :
       logging.info('[TestPrintOnly]Send pushover event')
       return
    m = '我家F門 Event px=%d' % q
    t = threading.Thread(target=pushoverPost, args=(m,))
    t.start()