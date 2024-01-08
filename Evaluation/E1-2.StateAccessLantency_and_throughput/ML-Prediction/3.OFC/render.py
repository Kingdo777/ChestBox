import json
import os
import sys
import time
import numpy as np
import pickle
from PIL import Image
import redis
from tool import TimeStatistics

data_dir = "/app/data"


def render():
    time_statistics = TimeStatistics()
    ######################################################################
    time_statistics.dot()
    redis_client = redis.Redis(
        host="222.20.94.66",
        port=6379)
    time_statistics.add_invoke_time()

    ######################################################################
    time_statistics.dot()
    x = pickle.loads(redis_client.get("x"))
    time_statistics.add_access_time()

    ######################################################################
    time_statistics.dot()
    labels = json.load(open(os.path.join(data_dir, 'labels.json')))
    text = ("Top 1 Prediction: index({}), class({}), probability({})".
            format(x.argmax(), labels[str(x.argmax())], x.max()))
    time_statistics.add_exec_time()

    print(time_statistics)
    # print(text)


if __name__ == '__main__':
    render()
