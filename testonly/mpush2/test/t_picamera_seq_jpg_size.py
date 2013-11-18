'''
https://github.com/waveform80/picamera
'''
import time, picamera, io, threading
from PIL import Image
from numpy import *

# 1920x1080 FULL HD
# 1280x720 (720p)
# 640x480
w,h = 640,480
# w,h = 1920,1080
# w,h = 1280,720

temps = io.BytesIO()
 
def getPilJpgSize(im):
    im.save(temps, 'jpeg')
    size = temps.tell()
    temps.seek(0)
    stream.truncate()
    return size

def readPilCropJpg(stream, dim=2):
     # 640x480 crop 4x4/fps 1.7
     # 640x480 cr0p 8x8/fps 1.3
     # 720p crop 4x4 /fps 0.85
     # 720p crop 8x8 /fps 0.75
     # 1920x1080 crop 4x4 /fps 0.45
    # 1920x1080 crop 8x8 /fps 0.4
    stream.seek(0)
    im2 = Image.open(stream)
    # getdata cost 5fps
    # imdata = im2.getdata()
    wx = int(w / dim)
    hy = int(h / dim)
    sarr = []
    for xi in xrange(dim):
        for yi in xrange(dim):
            x, y = xi * wx, yi * hy
            print x, y
            imcrop = im2.crop((x, y, x + wx, y + hy))
            sarr.append(getPilJpgSize(imcrop))
            
    print sarr
    
    # raise cpu loading 100% without sleep 
    # sleep cost 2 fps
    time.sleep(0.2)

def readPilResize(stream, dim=2):
    # 1080p 8x8 2.2fps
    # 720p 8x8 3.5fps
    # 640x480 5.8fps
    stream.seek(0)
    im2 = Image.open(stream)
    # getdata cost 5fps
    wx = int(w / dim)
    hy = int(h / dim)
    size = wx,hy
    im2.thumbnail(size, Image.ANTIALIAS)
    imgray = ImageOps.grayscale(im2)
    # print list(imgray.getdata())
    imdata = im2.getdata()
    #print im2.info
    #print list(imdata)
    #print im2.getbbox()
    
    # raise cpu loading 100% without sleep 
    # sleep cost 2 fps
    time.sleep(0.1)

def readPilHistogram(stream):
    stream.seek(0)
    im = Image.open(stream)
    hl = im.histogram()


with picamera.PiCamera() as camera:
    camera.resolution = (w, h)
    camera.framerate = 10
    time.sleep(2)
    start = time.time()
    stream = io.BytesIO()
    count = 0
    # Use the video-port for captures...
    for foo in camera.capture_continuous(stream, 'jpeg',
                                             use_video_port=True):
        size = stream.tell()   
        #readPilHistogram(stream)
        #readPilResize(stream,dim=8)
        #readPilCropJpg(stream, dim=8)
            
        # stream.seek(0)
        # connection.write(stream.read())
        dtime = time.time() - start
        if dtime > 10:
            break
        stream.seek(0)
        stream.truncate()
        count += 1
        print('Size: %d /Captured %d images at %.2ffps' % (size, count, count / dtime))

