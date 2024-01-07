import json
import logging
import os
import sys
import time
import numpy as np
import pickle
from PIL import Image
import redis
import socket
from tool import TimeStatistics, send_msg, recv_msg, predict_server_port, render_server_port

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

data_dir = "/app/data"


def predict():
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", predict_server_port))
    server_socket.listen(5)
    time_statistics.add_invoke_time()

    client_socket, addr = server_socket.accept()

    ######################################################################
    time_statistics.dot()
    resize_img = pickle.loads(recv_msg(client_socket))
    send_msg(client_socket, b"OK")
    client_socket.close()
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
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("222.20.94.67", render_server_port))
    send_msg(client_socket, pickle.dumps(x))
    data = recv_msg(client_socket)
    if data.decode() != "OK":
        raise RuntimeError("Not OK!")
    client_socket.close()
    time_statistics.add_access_time()

    print(time_statistics)


if __name__ == '__main__':
    predict()
