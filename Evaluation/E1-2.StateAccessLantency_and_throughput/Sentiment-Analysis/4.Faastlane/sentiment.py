import json
import nltk
import time

from tool import TimeStatistics

nltk.data.path.append('/app/nltk_data/')
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def main(event):
    time_statistics = TimeStatistics().from_list(event["time_statistics"])
    ######################################################################
    data = event["data"]
    time_statistics.add_access_time(event["start_time"])

    ######################################################################
    time_statistics.dot()
    body_list = json.loads(data)
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
    result = {"sentiments": json.dumps(sentiments)}
    time_statistics.add_exec_time()

    result["time_statistics"] = time_statistics.to_list()
    result["start_time"] = 1000 * time.time()

    return result
