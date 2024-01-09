import boto3
import pickle
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
    sentiments_data = redis_client.get('sentiments_data')
    time_statistics.add_access_time()

    ######################################################################
    time_statistics.dot()
    sentiments = pickle.loads(sentiments_data)
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

    print(time_statistics)


if __name__ == '__main__':
    main()
