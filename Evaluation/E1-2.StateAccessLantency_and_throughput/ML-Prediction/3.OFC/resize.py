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


def main():
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    image = Image.open(os.path.join(data_dir, 'panda.jpg'))
    img = np.array(image.resize((224, 224))).astype(float) / 128 - 1
    resize_img = img.reshape(1, 224, 224, 3)
    time_statistics.add_exec_time()

    ######################################################################
    time_statistics.dot()
    redis_client = redis.Redis(
        host="127.0.0.1",
        port=6379)
    time_statistics.add_invoke_time()

    ######################################################################
    time_statistics.dot()
    redis_client.set("resize_img", pickle.dumps(resize_img))
    time_statistics.add_access_time()
    print(time_statistics)

    # print("resize-image-size: ", sys.getsizeof(pickle.dumps(resize_img)))


if __name__ == '__main__':
    main()
