import nltk
import pickle
import redis
import socket
from tool import TimeStatistics, send_msg, recv_msg, analytics_server_port

nltk.data.path.append('/app/nltk_data/')
from nltk.tokenize import word_tokenize


def analytics():
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", analytics_server_port))
    server_socket.listen(5)
    time_statistics.add_invoke_time()

    client_socket, addr = server_socket.accept()

    ######################################################################
    time_statistics.dot()
    masked_message = recv_msg(client_socket).decode()
    send_msg(client_socket, b"OK")
    client_socket.close()
    time_statistics.add_access_time()

    ######################################################################
    time_statistics.dot()
    tokens = word_tokenize(masked_message)
    time_statistics.add_exec_time()

    # print(tokens)
    print(time_statistics)


if __name__ == '__main__':
    analytics()
