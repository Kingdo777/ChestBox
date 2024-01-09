import json
import os

import boto3
import numpy as np

from tool import TimeStatistics

data_dir = "/app/data"


def main(event):
    time_statistics = TimeStatistics().from_list(event["time_statistics"])
    ######################################################################
    sentiments_data = event["sentiments"]
    time_statistics.add_access_time(event["start_time"])

    ######################################################################
    time_statistics.dot()
    sentiments = json.loads(sentiments_data)
    sns = boto3.client('sns', aws_access_key_id="AKIAQ4WHHPCKGVH4HO6S",
                       aws_secret_access_key="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",
                       region_name="us-east-1")
    for sentiment in sentiments:
        message = ('Review (ID = {}) of {} (ID = {}) received with negative results '
                   'from sentiment analysis. Feedback from Customer (ID = {}): "{}"').format(
            sentiment['reviewID'], sentiment['reviewType'],
            sentiment['productID'], sentiment['customerID'], sentiment['feedback'])
        # print(message)
        # construct message from input data and publish via SNS
        # sns.publish(
        #     TopicArn='arn:aws:sns:XXXXXXXXXXXXXXXX:my-SNS-topic',
        #     Subject='Negative Review Received',
        #     Message=message
        # )
    time_statistics.add_exec_time()

    return str(time_statistics)
