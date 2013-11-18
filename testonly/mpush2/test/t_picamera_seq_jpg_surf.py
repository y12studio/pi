'''
https://github.com/waveform80/picamera
'''
import time, picamera, io, threading
from PIL import Image
from numpy import *



w, h = 320, 240
temps = io.BytesIO()
imarr = []
 
with picamera.PiCamera() as camera:
    camera.resolution = (w, h)
    camera.framerate = 2
    time.sleep(2)
    start = time.time()
    stream = io.BytesIO()
    count = 0
    for foo in camera.capture_continuous(stream, 'jpeg',
                                             use_video_port=True):
        size = stream.tell()           
        stream.seek(0)
        imarr.append(Image.open(stream))
        dtime = time.time() - start
        if dtime > 5:
            break
        stream.seek(0)
        stream.truncate()
        count += 1
        print('Size: %d /Captured %d images at %.2ffps' % (size, count, count / dtime))

print cv2.__version__
surfdetect = cv2.FeatureDetector_create('SURF')
surfextract = cv2.DescriptorExtractor_create('SURF')

img1 = imarr[0]
img2 = img1.filter(ImageFilter.FIND_EDGES)
img2.save('surf_find_edge.jpg')
keys1 = surfdetect.detect(img1)
keys2 = surfdetect.detect(img2)
keys1,features1 = surfextrace.compute(img1,keys1)
keys1,features2 = surfextrace.compute(img2,keys2)


