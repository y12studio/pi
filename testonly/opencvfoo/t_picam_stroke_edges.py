
import io, time, cv2, picamera
import numpy as np
import tornado.ioloop
import tornado.web

# Create the in-memory stream
stream = io.BytesIO()
imgBefore = None
imgAfter = None
cam = picamera.PiCamera()

def initCameraImg(w, h):
    cam.resolution = (w, h)
    cam.vflip = True
    cam.start_preview()
    time.sleep(2)

def getCameraImg():
    cam.capture(stream, format='jpeg')
    r = stream.getvalue()
    stream.seek(0)
    return r
 
def streamToCvImgArr(streamValue):
    data = np.fromstring(streamValue, dtype=np.uint8)
    r = cv2.imdecode(data, 1)
    return r

def cvImgArrToStream(cvImg):
    result, jpg = cv2.imencode('.jpg', cvImg, [1, 90])
    jpgbytes = np.array(jpg).tostring()
    return jpgbytes

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("<html><body><h4>BEFORE</h4>")
        self.write('<a href="img.jpg?v=before" target="_blank"><img src="img.jpg?v=before" width="320" height="240"/></a>')
        self.write("<h4>AFTER</h4>")
        self.write('<a href="img.jpg?v=after" target="_blank"><img src="img.jpg?v=after" width="320" height="240"/></a>')
        self.write("</body></html>")
        
def handleImgWork():
    global imgBefore,imgAfter
    imgBefore = getCameraImg()

    cvImgArr1 = streamToCvImgArr(imgBefore)
    cvImgArr2 = np.copy(cvImgArr1)
    
    #processRoi(cvImgArr1,cvImgArr2)
    #processRecolorRC(cvImgArr1,cvImgArr2)
    processStrokeEdges(cvImgArr1,cvImgArr2)
    imgAfter = cvImgArrToStream(cvImgArr2)

class ImageHandler(tornado.web.RequestHandler):
    def get(self):
        handleImgWork()
        v = self.get_argument("v")    
        if v == 'before':
            img = imgBefore
        else:
            img = imgAfter            
        self.set_header('Content-type', 'image/jpeg')
        self.set_header('Content-length', len(img))
        self.write(img)
 
application = tornado.web.Application([
 (r"/", MainHandler),
 (r"/img.jpg", ImageHandler),
])

def processRoi(src,dst):
    roi = src[280:340, 100:160]
    dst[273:333, 300:360] = roi
    
def processRecolorRC(src,dst):
    b,g,r = cv2.split(src)
    cv2.addWeighted(b,0.5,g,0.5,0,b)
    cv2.merge((b,g,r),dst)

def processStrokeEdges(src,dst,blurKsize=7,edgeKsize=5):
    if blurKsize >=3 :
        blurredSrc = cv2.medianBlur(src,blurKsize)
        graySrc = cv2.cvtColor(blurredSrc,cv2.COLOR_BGR2GRAY)
    else:
        graySrc = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
    cv2.Laplacian(graySrc, cv2.cv.CV_8U, graySrc, ksize = edgeKsize)
    normalizedInverseAlpha = (1.0 / 255) * (255 - graySrc)
    channels = cv2.split(src)
    for channel in channels:
        channel[:] = channel * normalizedInverseAlpha
    cv2.merge(channels, dst)
    
if __name__ == "__main__":
    try:
        initCameraImg(640,480)
        print('Starting server , see http://raspberry_ip:8888/')
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
    finally:
        cam.stop_preview()
        cam.close()

