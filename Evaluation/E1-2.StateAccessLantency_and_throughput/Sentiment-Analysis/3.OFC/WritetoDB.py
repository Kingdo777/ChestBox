import pickle
import time

import boto3
import redis
from tool import TimeStatistics, redis_host


def main():
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    redis_client = redis.Redis(
        host=redis_host,
        port=6379)
    time_statistics.add_invoke_time()

    ######################################################################
    time_statistics.dot()
    sentiments_data = redis_client.get("sentiments_data")
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
