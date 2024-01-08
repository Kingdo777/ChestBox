import json
import os
import time

import numpy as np
from PIL import Image

from tool import TimeStatistics

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

data_dir = "/app/data"


def main(event):
    time_statistics = TimeStatistics().from_list(event["time_statistics"])
    ######################################################################
    resize_img = event["resize_img"]
    time_statistics.add_access_time(event["start_time"])

    ######################################################################
    time_statistics.dot()
    gd = tf.compat.v1.GraphDef. \
        FromString(open(os.path.join(data_dir, 'mobilenet_v2_1.0_224_frozen.pb'), 'rb').read())
    inp, predictions = tf. \
        import_graph_def(gd, return_elements=['input:0', 'MobilenetV2/Predictions/Reshape_1:0'])
    with tf.compat.v1.Session(graph=inp.graph):
        x = predictions.eval(feed_dict={inp: np.array(json.loads(resize_img))})
    result = {"x": json.dumps(x.tolist())}
    time_statistics.add_exec_time()

    result["time_statistics"] = time_statistics.to_list()
    result["start_time"] = 1000 * time.time()

    return result
