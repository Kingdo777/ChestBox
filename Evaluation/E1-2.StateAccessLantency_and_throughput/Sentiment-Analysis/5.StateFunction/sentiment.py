import os
import pickle
import time
import nltk
import ipc

os.environ['STATE_FUNCTION_LOG_LEVEL'] = 'off'
import statefunction as sf
from tool import TimeStatistics

nltk.data.path.append('/app/nltk_data/')
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

Action_Pipe_Key = 0x1112


def main():
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    msg = ipc.create_msg(Action_Pipe_Key)
    bucket = sf.get_bucket("kingdo", True, Action_Pipe_Key)
    msg.destroy()
    time_statistics.add_invoke_time()

    ######################################################################
    time_statistics.dot()
    data = bucket.get_bytes("body_list")
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
    # print(size := len(sentiments_data))
    bucket.set("sentiments_data", sentiments_data)
    time_statistics.add_access_time()

    print(time_statistics)


if __name__ == "__main__":
    main()
