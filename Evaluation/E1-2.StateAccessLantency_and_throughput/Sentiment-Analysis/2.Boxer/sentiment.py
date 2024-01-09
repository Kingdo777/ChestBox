import pickle
import socket
import time
import nltk
import redis
from tool import TimeStatistics
from tool import sentiment_server_port, WritetoDB_server_port, publishsns_server_port, send_msg, recv_msg

nltk.data.path.append('/app/nltk_data/')
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def main():
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", sentiment_server_port))
    server_socket.listen(5)
    time_statistics.add_invoke_time()

    client_socket, addr = server_socket.accept()

    ######################################################################
    time_statistics.dot()
    data = recv_msg(client_socket)
    send_msg(client_socket, b"OK")
    client_socket.close()
    time_statistics.add_access_time()

    ######################################################################
    time_statistics.dot()
    body_list = pickle.loads(data)
    sid = SentimentIntensityAnalyzer()
    sentiments = []
    for body in body_list:
        feedback = body['feedback']
        scores = sid.polarity_scores(feedback)
        if scores['compound'] > 0:
            sentiment = 1
        elif scores['compound'] == 0:
            sentiment = 0
        else:
            sentiment = -1
        sentiments.append({'sentiment': sentiment,
                           'reviewType': body['reviewType'] + 0,
                           'reviewID': (body['reviewID'] + '0')[:-1],
                           'customerID': (body['customerID'] + '0')[:-1],
                           'productID': (body['productID'] + '0')[:-1],
                           'feedback': (body['feedback'] + '0')[:-1]})
    sentiments_data = pickle.dumps(sentiments)
    time_statistics.add_exec_time()

    ######################################################################
    time_statistics.dot()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("222.20.94.67", WritetoDB_server_port))
    send_msg(client_socket, sentiments_data)
    data = recv_msg(client_socket)
    if data.decode() != "OK":
        raise RuntimeError("Not OK!")
    client_socket.close()
    time_statistics.add_access_time()

    ######################################################################
    time_statistics.dot()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("222.20.94.67", publishsns_server_port))
    send_msg(client_socket, sentiments_data)
    data = recv_msg(client_socket)
    if data.decode() != "OK":
        raise RuntimeError("Not OK!")
    client_socket.close()
    time_statistics.add_access_time()

    print(time_statistics)


if __name__ == "__main__":
    main()
