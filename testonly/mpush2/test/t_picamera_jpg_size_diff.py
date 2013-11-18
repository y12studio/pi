'''
https://github.com/waveform80/picamera
'''
import time,picamera,io
from PIL import Image

# Create the in-memory stream
stream = io.BytesIO()
with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.start_preview()
    time.sleep(2)
    start = time.time()
    size1 = 0;
    for i in range(20):
        camera.capture(stream, format='jpeg')
        
        size2 = stream.tell()
        diff = abs(size2 - size1)
        print diff
        size1 = size2
        # "Rewind" the stream to the beginning so we can read its content
        stream.seek(0)
        #image = Image.open(stream)
        #print image.format, image.size, image.mode
        #stream.seek(0)
    print('Captured 20 images at %.2ffps' % (20 / (time.time() - start)))
    camera.stop_preview()
