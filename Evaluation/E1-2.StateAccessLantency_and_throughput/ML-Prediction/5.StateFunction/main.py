import json
import os
import subprocess
import sys
import time
from os.path import dirname
import ipc
import docker
import numpy as np
import pickle
from PIL import Image

os.environ['STATE_FUNCTION_LOG_LEVEL'] = 'off'
import statefunction as df

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

venv_path = os.path.join(dirname(dirname(dirname(dirname(dirname(os.path.abspath(__file__)))))), "venv")
data_dir = os.path.join(dirname(dirname(os.path.abspath(__file__))), "data")
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

    def reset(self):
        self.exec_time = 0
        self.invoke_time = 0
        self.access_time = 0
        self.resides_time = 0

    def __str__(self):
        return "{:.2f},{:.2f},{:.2f},{:.2f}".format(
            self.exec_time, self.invoke_time, self.access_time, self.resides_time)


class ImagePredictor:
    def __init__(self, enable_pipe):
        self.enable_pipe = enable_pipe
        self.time_statistics = TimeStatistics()
        self.gd = tf.compat.v1.GraphDef. \
            FromString(open(os.path.join(data_dir, 'mobilenet_v2_1.0_224_frozen.pb'), 'rb').read())
        self.inp, self.predictions = tf. \
            import_graph_def(self.gd, return_elements=['input:0', 'MobilenetV2/Predictions/Reshape_1:0'])

    def resize(self, image_path):
        ######################################################################
        self.time_statistics.dot()
        image = Image.open(image_path)
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
        with tf.compat.v1.Session(graph=self.inp.graph):
            x = self.predictions.eval(feed_dict={self.inp: resize_img})
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
        labels = json.load(open(os.path.join(data_dir, 'labels.json')))
        text = ("Top 1 Prediction: index({}), class({}), probability({})".
                format(x.argmax(), labels[str(x.argmax())], x.max()))
        self.time_statistics.add_exec_time()
        return text

    def workflow(self, image_path):
        self.resize(image_path)

        start_time = 1000 * time.time()
        self.predict()
        self.time_statistics.add_resides_time(start_time)

        start_time = 1000 * time.time()
        result = self.render()
        self.time_statistics.add_resides_time(start_time)

        print(self.time_statistics, "\t\t\t\t", result, flush=True)

        time_statistics_info = str(self.time_statistics)
        self.time_statistics.reset()

        return time_statistics_info


def run_predict(image_path, loop):
    msg = ipc.create_msg(Action_Pipe_Key)
    results = []
    img_predictor = ImagePredictor(True)
    for i in range(loop):
        results.append(img_predictor.workflow(image_path))
    msg.destroy()
    return results


def main(loop: int = 1):
    image_path = os.path.join(data_dir, "panda.jpg")
    try:
        result = run_predict(image_path, loop)
        record_file = "results/summary"
        with open(record_file, "w") as f:
            f.write("exec_time,invoke_time,access_time,resides_time\n")
            for i in result:
                f.write(str(i) + "\n")
    except Exception as e:
        print(e)


def join_docker_namespace():
    # docker inspect -f '{{.State.Pid}}' <container_id_or_name>
    container_pid = docker.from_env().api.inspect_container("state-function")['State']['Pid']
    subprocess.run(['nsenter', '--target', f"{container_pid}", '--ipc',
                    '--', os.path.join(venv_path, "bin/python3"), sys.argv[0], 'run'])


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "run":
        main(1000)
        exit(0)
    else:
        try:
            # docker stop state-function
            docker.from_env().api.stop("state-function")
            print("stop old state-function container")
        except Exception as e:
            print(e)

        try:
            # docker run -d --rm --name state-function kingdo/state-function
            docker.from_env().containers.run("kingdo/state-function", detach=True, name="state-function", remove=True)
            print("start new state-function container")
        except Exception as e:
            print(e)
            exit(0)

        join_docker_namespace()
