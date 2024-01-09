import pickle

import boto3
import socket
from tool import TimeStatistics, WritetoDB_server_port, send_msg, recv_msg


def main():
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", WritetoDB_server_port))
    server_socket.listen(5)
    time_statistics.add_invoke_time()

    client_socket, addr = server_socket.accept()

    ######################################################################
    time_statistics.dot()
    sentiments_data = recv_msg(client_socket)
    send_msg(client_socket, b"OK")
    client_socket.close()
    time_statistics.add_access_time()

    ######################################################################
    time_statistics.dot()
    sentiments = pickle.loads(sentiments_data)
    dynamodb = boto3.client('dynamodb', aws_access_key_id="AKIAQ4WHHPCKGVH4HO6S",
                            aws_secret_access_key="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",
                            region_name="us-east-1")
    for sentiment in sentiments:
        # select correct table based on input data
        if sentiment['reviewType'] == 0:
            tableName = 'faastlane-products-table'
        elif sentiment['reviewType'] == 1:
            tableName = 'faastlane-services-table'
        else:
            raise Exception("Input review is neither Product nor Service")
    time_statistics.add_exec_time()

    print(time_statistics)


if __name__ == "__main__":
    main()
