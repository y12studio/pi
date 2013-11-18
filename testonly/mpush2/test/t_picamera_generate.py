'''
https://github.com/waveform80/picamera
'''
import time, picamera, io, threading
from PIL import Image, ImageChops

w = 640
h = 480

class ImageProcessorSizeDiff:
    
    def __init__(self):
        self.stream = io.BytesIO()
        self.count = 0
        self.start = time.time()
        self.im1 = 0
    
    def diff(self, im2):
        if self.im1 == 0:
            return
        return  abs(im2 - self.im1)

    def run(self):
        # This method runs in a separate thread
       
        self.count += 1
        try:
            im2 = self.stream.tell()
            # print im2
            self.stream.seek(0)
            q = self.diff(im2)
            print q
            self.im1 = im2
        finally:
            # Reset the stream and event
            self.stream.seek(0)
            self.stream.truncate()
            # time.sleep(0.2)
        print('Captured %d images at %.2ffps' % (self.count, (self.count / (time.time() - self.start))))


class ImageProcessorPil:
    
    def __init__(self):
        self.stream = io.BytesIO()
        self.count = 0
        self.start = time.time()
        self.im1 = None
    
    def rgbTo32bitInt(self, rgb):
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        return r * 256 ^ 2 + g * 256 + b
    
    def testImageLoadlist(self, im2):
        r = []
        pix = im2.load()
        for x in range(w) :
            for y in range(h):
                rgbv = self.rgbTo32bitInt(pix[x, y])
                r.append(rgbv)
        return r
    
    def diff(self, im2):
        if self.im1 == None:
            return 
        diff = ImageChops.difference(im2, self.im1)
        dlist = list(diff.getdata())
        rlist = map(self.rgbTo32bitInt, dlist)
        total = 0
        for pix in dlist:
            total += sum(pix)
        return (total, rlist)

    def run(self):
        # This method runs in a separate thread
      
        self.count += 1
        try:
            self.stream.seek(0)
            # Read the image and do some processing on it
            im2 = Image.open(self.stream)
            # print im2.format, im2.size, im2.mode
            imList = map(self.rgbTo32bitInt, list(im2.getdata()))
            # self.testImageLoadlist(im2)
            q = self.diff(im2)
            # q[0] = total_diff_pixel/q[1] rgbvalue list
            self.im1 = im2
           
        finally:
            # Reset the stream and event
            self.stream.seek(0)
            self.stream.truncate()
            # keep cpu cool
            # time.sleep(0.1)
        print('Captured %d images at %.2ffps' % (self.count, (self.count / (time.time() - self.start))))


'''
Pil 
100x100 fps1.8 cpu 95%
320x240 fps0.3 cpu 95%
'''
# processor = ImageProcessorPil()
'''
jpeg size diff
100x100 fps-depend-capture sleep-none cpu 1%
320x240 fps-depend-capture sleep-none cpu 1%
'''
processor = ImageProcessorSizeDiff()
count = 0
def streams():
    global count
    while count < 20:
        yield processor.stream
        processor.run()
        count+=1

with picamera.PiCamera() as camera:
    camera.resolution = (w, h)
    camera.framerate = 5
    camera.start_preview()
    time.sleep(2)
    processor.start = time.time()
    camera.capture_sequence(streams(),'jpeg' ,use_video_port=True)

# Shut down the processors in an orderly fashion
processor.terminated = True
