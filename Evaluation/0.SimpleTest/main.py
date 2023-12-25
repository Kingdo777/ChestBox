import json
import os
import sys
import time
import ipc

import numpy as np
import pickle
from PIL import Image
import statefunction as df
import tensorflow as tf

# data/mobilenet_v2_1.0_224_frozen.pb downloaded from :
# https://storage.googleapis.com/mobilenet_v2/checkpoints/mobilenet_v2_1.0_224.tgz or
# https://github.com/tensorflow/models/tree/master/research/slim

# the label file is downloaded from:
# https://github.com/leferrad/tensorflow-mobilenet/blob/master/imagenet/labels.json and info is from:
# https://deeplearning.cms.waikato.ac.nz/user-guide/class-maps/IMAGENET/

Action_Pipe_Key = 0x1111


class TimeStatistics:
    def __init__(self):
        self.exec_time = 0
        self.invoke_time = 0
        self.access_time = 0
        self.resides_time = 0
        self.start_time = 1000 * time.time()

    def dot(self):
        self.start_time = 1000 * time.time()

    def add_exec_time(self):
        self.exec_time += (1000 * time.time() - self.start_time)

    def add_invoke_time(self):
        self.invoke_time += (1000 * time.time() - self.start_time)

    def add_access_time(self):
        self.access_time += (1000 * time.time() - self.start_time)

    def add_resides_time(self, start_time):
        self.resides_time += (1000 * time.time() - start_time)

    def __str__(self):
        return "{}, {}, {}, {}".format(
            self.exec_time, self.invoke_time, self.access_time, self.resides_time)


class ImagePredictor:
    def __init__(self, enable_pipe, image_path):
        self.enable_pipe = enable_pipe
        self.image_path = image_path
        self.time_statistics = TimeStatistics()

    def resize(self):
        ######################################################################
        self.time_statistics.dot()
        image = Image.open(self.image_path)
        img = np.array(image.resize((224, 224))).astype(float) / 128 - 1
        resize_img = img.reshape(1, 224, 224, 3)
        self.time_statistics.add_exec_time()

        ######################################################################
        self.time_statistics.dot()
        bucket = df.create_bucket("kingdo", 1024 * 1024 * 4, self.enable_pipe, Action_Pipe_Key)
        self.time_statistics.add_invoke_time()

        ######################################################################
        self.time_statistics.dot()
        bucket.set("resize_img", pickle.dumps(resize_img))
        self.time_statistics.add_access_time()

    def predict(self):
        ######################################################################
        self.time_statistics.dot()
        bucket = df.get_bucket("kingdo", self.enable_pipe, Action_Pipe_Key)
        self.time_statistics.add_invoke_time()

        ######################################################################
        self.time_statistics.dot()
        resize_img = pickle.loads(bucket.get_bytes("resize_img"))
        self.time_statistics.add_access_time()

        ######################################################################
        self.time_statistics.dot()
        gd = tf.compat.v1.GraphDef.FromString(open('data/mobilenet_v2_1.0_224_frozen.pb', 'rb').read())
        inp, predictions = tf.import_graph_def(gd, return_elements=['input:0', 'MobilenetV2/Predictions/Reshape_1:0'])
        with tf.compat.v1.Session(graph=inp.graph):
            x = predictions.eval(feed_dict={inp: resize_img})
        self.time_statistics.add_exec_time()

        ######################################################################
        self.time_statistics.dot()
        bucket.set("x", pickle.dumps(x))
        self.time_statistics.add_access_time()

    def render(self):
        ######################################################################
        self.time_statistics.dot()
        bucket = df.get_bucket("kingdo", self.enable_pipe, Action_Pipe_Key)
        self.time_statistics.add_invoke_time()

        ######################################################################
        self.time_statistics.dot()
        x = pickle.loads(bucket.get_bytes("x"))
        self.time_statistics.add_access_time()

        ######################################################################
        self.time_statistics.dot()
        bucket.destroy()
        self.time_statistics.add_invoke_time()

        ######################################################################
        self.time_statistics.dot()
        labels = json.load(open('data/labels.json'))
        text = ("Top 1 Prediction: index({}), class({}), probability({})".
                format(x.argmax(), labels[str(x.argmax())], x.max()))
        self.time_statistics.add_exec_time()
        return text

    def workflow(self):
        self.resize()

        start_time = 1000 * time.time()
        self.predict()
        self.time_statistics.add_resides_time(start_time)

        start_time = 1000 * time.time()
        print(self.render())
        self.time_statistics.add_resides_time(start_time)

        return str(self.time_statistics)


def run_predict(image_path_lists, enable_pipe):
    msg = None
    if enable_pipe:
        msg = ipc.create_msg(Action_Pipe_Key)

    result = []
    for image in image_path_lists:
        image_predictor = ImagePredictor(enable_pipe, image)
        result.append(image_predictor.workflow())

    if enable_pipe:
        msg.destroy()
    return result


def main(argc, argv):
    enable_pipe = False
    if argc == 2:
        enable_pipe = True if argv[1] == "True" else False

    image_path_lists = []
    image_directory = "./data/img/photos_of_animals_and_plants"
    for filename in os.listdir(image_directory):
        image_path = os.path.join(image_directory, filename)
        if (os.path.isfile(image_path) and
                (filename.endswith(".jpg") or filename.endswith(".png"))):
            image_path_lists.append(image_path)
    image_path_lists.sort()

    image_path_lists = image_path_lists[:100]

    try:
        result = run_predict(image_path_lists, enable_pipe)
        record_file = "result/result_with_pipe.txt" if enable_pipe else "result/result_without_pipe.txt"
        with open(record_file, "w") as f:
            f.write("exec_time, invoke_time, access_time, resides_time\n")
            for i in result:
                f.write(str(i) + "\n")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
    # pass
