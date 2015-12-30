import tornado.ioloop
import tornado.web
import os
import urllib
import json
import traceback
import numpy as np
from tornado.escape import json_encode

import sys
sys.path.append('pysample')
import model

x = tf.placeholder("float", [None, 784])
sess = tf.Session()

with tf.variable_scope("simple"):
    y1, variables = model.simple(x)
saver = tf.train.Saver(variables)
saver.restore(sess, "pysample/data/simple.ckpt")


def simple(input):
    return sess.run(y1, feed_dict={x: input}).flatten().tolist()

with tf.variable_scope("convolutional"):
    keep_prob = tf.placeholder("float")
    y2, variables = model.convolutional(x, keep_prob)
saver = tf.train.Saver(variables)
saver.restore(sess, "pysample/data/convolutional.ckpt")


def convolutional(input):
    return sess.run(y2, feed_dict={x: input, keep_prob: 1.0}).flatten().tolist()


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")


class MNISTHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("mnist")

    def post(self):
        self.set_header("Content-Type", "json/application")
        input = ((255 - np.array(self.json_args, dtype=np.uint8)) /
                 255.0).reshape(1, 784)
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
