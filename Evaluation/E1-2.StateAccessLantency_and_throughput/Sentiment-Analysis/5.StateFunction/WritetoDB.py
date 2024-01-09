import os
import pickle
import time
import ipc

import boto3
from tool import TimeStatistics

os.environ['STATE_FUNCTION_LOG_LEVEL'] = 'off'
import statefunction as sf

Action_Pipe_Key = 0x1113


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
    sentiments_data = bucket.get_bytes("sentiments_data")
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
