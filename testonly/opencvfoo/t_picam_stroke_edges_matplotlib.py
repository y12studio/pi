
import io, time, cv2, picamera
import numpy as np
import tornado.ioloop
import tornado.web
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Create the in-memory stream
stream = io.BytesIO()
imgBefore = None
imgAfter = None
cam = picamera.PiCamera()
calcCount = 0

def initCameraImg(w, h):
    cam.resolution = (w, h)
    cam.vflip = True
    cam.start_preview()
    time.sleep(2)

def getCameraImg():
    stream.seek(0)
    cam.capture(stream, format='jpeg')
    r = stream.getvalue()
    return r
 
def streamToCvImgArr(streamValue):
    data = np.fromstring(streamValue, dtype=np.uint8)
    r = cv2.imdecode(data, 1)
    return r

def cvImgArrToStream(cvImg):
    result, jpg = cv2.imencode('.jpg', cvImg, [1, 90])
    jpgbytes = np.array(jpg).tostring()
    return jpgbytes

def plotToPng():
    plt.grid(True)
    stream.seek(0)
    plt.savefig(stream, format='png')
    image = stream.getvalue()
    return image

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("<html><body><h4>BEFORE</h4>")
        self.write('<a href="img.jpg?v=before" target="_blank"><img src="img.jpg?v=before" width="320" height="240"/></a>')
        self.write("<h4>AFTER</h4>")
        # matplotlib export png only
        self.write('<a href="img.png?v=after" target="_blank"><img src="img.png?v=after" width="320" height="240"/></a>')
        self.write("</body></html>")
        
def handleImgWork():
    global imgBefore,imgAfter,calcCount
    # only run once
    if imgAfter is not None:
        return
    
    calcCount+=1
    imgBefore = getCameraImg()

    cvImgArr1 = streamToCvImgArr(imgBefore)
    cvImgArr21 = np.copy(cvImgArr1)
    cvImgArr22 = np.copy(cvImgArr1)
    cvImgArr23 = np.copy(cvImgArr1)
    
    processStrokeEdges(cvImgArr1,cvImgArr21,7,5)
    processStrokeEdges(cvImgArr1,cvImgArr22,5,5)
    processStrokeEdges(cvImgArr1,cvImgArr23,3,5)
    
    fig1 = plt.figure()
    plt.subplot(2,2,1)
    plt.imshow(cvImgArr1)
    plt.title("Original")
    plt.subplot(2,2,2)
    plt.imshow(cvImgArr21)
    plt.title("blur7,edge5")
    plt.subplot(2,2,3)
    plt.imshow(cvImgArr22)
    plt.title("blur5,edge5")
    plt.subplot(2,2,4)
    plt.imshow(cvImgArr23)
    plt.title("blur3,edge5")
    
    imgAfter = plotToPng()

class ImageHandler(tornado.web.RequestHandler):
    def get(self):
        handleImgWork()
        v = self.get_argument("v")    
        if v == 'before':
            img = imgBefore
            self.set_header('Content-type', 'image/jpeg')
        else:
            img = imgAfter
            # matplotlib export png only
            self.set_header('Content-type', 'image/png')
        self.set_header('Content-length', len(img))
        self.write(img)
 
application = tornado.web.Application([
 (r"/", MainHandler),
 (r"/img.*", ImageHandler),
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

