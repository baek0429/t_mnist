import tornado.ioloop
import tornado.web
import os
import urllib
import json, traceback
import numpy as np
from tornado.escape import json_encode

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class MNISTHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("mnist")
    def post(self):
        self.set_header("Content-Type", "text/plain")
        input = ((255 - np.array(self.json_args, dtype=np.uint8)) / 255.0).reshape(1, 784)
        obj = { 
            'foo': 'bar',
             '1': 2,
             'false': True 
            }
        self.write(json_encode(obj))

    def prepare(self):
        if self.request.headers["Content-Type"].startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/main", MNISTHandler),
    ],
    static_path=os.path.join(os.path.dirname(__file__), "js"),
    debug=True,
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()