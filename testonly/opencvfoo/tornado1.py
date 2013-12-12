import tornado.ioloop
import tornado.web
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
 
def genImage(freq):
    t = np.linspace(0, 10, 500)
    y = np.sin(t * freq * 2 * 3.141)
    fig1 = plt.figure()
    plt.plot(t, y)
    plt.xlabel('Time [s]')
    memdata = io.BytesIO()
    plt.grid(True)
    plt.savefig(memdata, format='png')
    image = memdata.getvalue()
    return image
 
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("<html><body><p>Hello, world</p>")
        self.write('<p><img src="test.png" /></p>')
        self.write("</body></html>")
 
class ImageHandler(tornado.web.RequestHandler):
    def get(self):
        image = genImage(1.4)
        self.set_header('Content-type', 'image/png')
        self.set_header('Content-length', len(image))
        self.write(image)
 
application = tornado.web.Application([
 (r"/", MainHandler),
 (r"/test.png", ImageHandler),
])
 
if __name__ == "__main__":
    print('Starting server')
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
