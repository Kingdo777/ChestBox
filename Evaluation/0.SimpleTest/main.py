import json
import time
import ipc

import numpy as np
import pickle
from PIL import Image
import statefunction as df

# data/mobilenet_v2_1.0_224_frozen.pb downloaded from :
# https://storage.googleapis.com/mobilenet_v2/checkpoints/mobilenet_v2_1.0_224.tgz or
# https://github.com/tensorflow/models/tree/master/research/slim

# the label file is downloaded from:
# https://github.com/leferrad/tensorflow-mobilenet/blob/master/imagenet/labels.json and info is from:
# https://deeplearning.cms.waikato.ac.nz/user-guide/class-maps/IMAGENET/

sf_time_used = 0

Action_Pipe_Key = 0x1111


def resize(path):
    global sf_time_used
    ######################################################################
    image = Image.open(path)
    img = np.array(image.resize((224, 224))).astype(float) / 128 - 1
    resize_img = img.reshape(1, 224, 224, 3)
    ######################################################################
    start_time = 1000 * time.time()
    bucket = df.create_bucket("kingdo", 1024 * 1024 * 4, True, Action_Pipe_Key)
    bucket.set("resize_img", pickle.dumps(resize_img))
    sf_time_used = 1000 * time.time() - start_time


def predict():
    global sf_time_used
    start_time = 1000 * time.time()
    bucket = df.get_bucket("kingdo", True, Action_Pipe_Key)
    resize_img = pickle.loads(bucket.get_bytes("resize_img"))
    sf_time_used += 1000 * time.time() - start_time
    ######################################################################
    import tensorflow as tf
    gd = tf.compat.v1.GraphDef.FromString(open('data/mobilenet_v2_1.0_224_frozen.pb', 'rb').read())
    inp, predictions = tf.import_graph_def(gd, return_elements=['input:0', 'MobilenetV2/Predictions/Reshape_1:0'])
    with tf.compat.v1.Session(graph=inp.graph):
        x = predictions.eval(feed_dict={inp: resize_img})
    ######################################################################
    start_time = 1000 * time.time()
    bucket.set("x", pickle.dumps(x))
    sf_time_used += 1000 * time.time() - start_time


def render():
    global sf_time_used
    start_time = 1000 * time.time()
    bucket = df.get_bucket("kingdo", True, Action_Pipe_Key)
    x = pickle.loads(bucket.get_bytes("x"))
    bucket.destroy()
    sf_time_used += 1000 * time.time() - start_time
    ######################################################################
    labels = json.load(open('data/labels.json'))
    text = ("Top 1 Prediction: index({}), class({}), probability({})".
            format(x.argmax(), labels[str(x.argmax())], x.max()))
    ######################################################################
    return text


if __name__ == '__main__':
    try:
        msg = ipc.create_msg(Action_Pipe_Key)
        resize("data/img/photos_of_animals_and_plants/img-0.jpg")
        predict()
        print(render())
        print("State-Function Overhead Time Used: {:.2f} ms".format(sf_time_used))
        msg.destroy()
    except Exception as e:
        print(e)
