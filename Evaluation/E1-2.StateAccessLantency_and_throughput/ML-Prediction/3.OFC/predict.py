import json
import os
import sys
import time
import numpy as np
import pickle
from PIL import Image
import redis
from tool import TimeStatistics

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

data_dir = "/app/data"


def predict():
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    redis_client = redis.Redis(
        host="127.0.0.1",
        port=6379)
    time_statistics.add_invoke_time()

    ######################################################################
    time_statistics.dot()
    resize_img = pickle.loads(redis_client.get("resize_img"))
    time_statistics.add_access_time()

    ######################################################################
    time_statistics.dot()
    gd = tf.compat.v1.GraphDef. \
        FromString(open(os.path.join(data_dir, 'mobilenet_v2_1.0_224_frozen.pb'), 'rb').read())
    inp, predictions = tf. \
        import_graph_def(gd, return_elements=['input:0', 'MobilenetV2/Predictions/Reshape_1:0'])
    with tf.compat.v1.Session(graph=inp.graph):
        x = predictions.eval(feed_dict={inp: resize_img})
    time_statistics.add_exec_time()

    ######################################################################
    time_statistics.dot()
    redis_client.set("x", pickle.dumps(x))
    time_statistics.add_access_time()

    # print("x-size: ", sys.getsizeof(pickle.dumps(x)))

    print(time_statistics)


if __name__ == '__main__':
    predict()
