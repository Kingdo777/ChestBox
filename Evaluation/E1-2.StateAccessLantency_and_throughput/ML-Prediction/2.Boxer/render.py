import json
import os
import sys
import time
import numpy as np
import pickle
from PIL import Image
import socket
from tool import TimeStatistics, send_msg, recv_msg, render_server_port

data_dir = "/app/data"


def render():
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", render_server_port))
    server_socket.listen(5)
    time_statistics.add_invoke_time()

    client_socket, addr = server_socket.accept()

    ######################################################################
    time_statistics.dot()
    x = pickle.loads(recv_msg(client_socket))
    send_msg(client_socket, b"OK")
    client_socket.close()
    time_statistics.add_access_time()

    ######################################################################
    time_statistics.dot()
    labels = json.load(open(os.path.join(data_dir, 'labels.json')))
    text = ("Top 1 Prediction: index({}), class({}), probability({})".
            format(x.argmax(), labels[str(x.argmax())], x.max()))
    time_statistics.add_exec_time()

    # print(text)
    print(time_statistics)


if __name__ == '__main__':
    render()
