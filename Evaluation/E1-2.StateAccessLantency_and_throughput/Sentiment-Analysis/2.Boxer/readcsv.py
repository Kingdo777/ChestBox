import csv
import pickle

import socket

from tool import TimeStatistics, send_msg, recv_msg, sentiment_server_port


def main():
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    body_list = []
    with open('/app/data/few_reviews.csv') as csvFile:
        # DictReader -> convert lines of CSV to OrderedDict
        for row in csv.DictReader(csvFile):
            # return just the first loop (row) results!
            body = {}
            for k, v in row.items():
                body[k] = int(v) if k == 'reviewType' else v
            body_list.append(body)
    data = pickle.dumps(body_list)
    time_statistics.add_exec_time()

    ######################################################################
    time_statistics.dot()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("222.20.94.67", sentiment_server_port))
    send_msg(client_socket, data)
    data = recv_msg(client_socket)
    if data.decode() != "OK":
        raise RuntimeError("Not OK!")
    client_socket.close()
    time_statistics.add_access_time()

    print(time_statistics)


if __name__ == "__main__":
    main()
