import json
import os
import socket
import sys
import time
import numpy as np
import pickle
from PIL import Image
from tool import TimeStatistics, send_msg, recv_msg, predict_server_port

data_dir = "/app/data"


def resize():
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    image = Image.open(os.path.join(data_dir, 'panda.jpg'))
    img = np.array(image.resize((224, 224))).astype(float) / 128 - 1
    resize_img = img.reshape(1, 224, 224, 3)
    time_statistics.add_exec_time()

    ######################################################################
    time_statistics.dot()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("222.20.94.67", predict_server_port))
    send_msg(client_socket, pickle.dumps(resize_img))
    data = recv_msg(client_socket)
    if data.decode() != "OK":
        raise RuntimeError("Not OK!")
    client_socket.close()
    time_statistics.add_access_time()

    print(time_statistics)


if __name__ == '__main__':
    resize()
