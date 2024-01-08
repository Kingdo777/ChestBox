import json
import logging
import os
import sys
import time
import numpy as np
import pickle
import socket
from tool import TimeStatistics, send_msg, recv_msg, anonymize_server_port, analytics_server_port


def mask_entities_in_message(message, entity_list):
    for entity in entity_list:
        message = message.replace(entity['Text'], '#' * len(entity['Text']))
    return message


def anonymize():
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", anonymize_server_port))
    server_socket.listen(5)
    time_statistics.add_invoke_time()

    client_socket, addr = server_socket.accept()

    ######################################################################
    time_statistics.dot()
    message_data = recv_msg(client_socket)
    send_msg(client_socket, b"OK")
    client_socket.close()
    time_statistics.add_access_time()

    ######################################################################
    time_statistics.dot()
    message = pickle.loads(message_data)
    masked_message = mask_entities_in_message(message["message"], message["entities"])
    time_statistics.add_exec_time()

    ######################################################################
    time_statistics.dot()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("222.20.94.67", analytics_server_port))
    send_msg(client_socket, masked_message.encode())
    data = recv_msg(client_socket)
    if data.decode() != "OK":
        raise RuntimeError("Not OK!")
    client_socket.close()
    time_statistics.add_access_time()

    print(time_statistics)


if __name__ == '__main__':
    anonymize()
