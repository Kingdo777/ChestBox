import json
import time

import boto3

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

    result = event
    result["time_statistics"] = time_statistics.to_list()
    result["start_time"] = 1000 * time.time()

    return result
