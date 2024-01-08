import json
import os
import sys
import time

import numpy as np
from PIL import Image
from tool import TimeStatistics

data_dir = "/app/data"


def main(event):
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    image = Image.open(os.path.join(data_dir, 'panda.jpg'))
    img = np.array(image.resize((224, 224))).astype(float) / 128 - 1
    resize_img = img.reshape(1, 224, 224, 3)
    result = {"resize_img": json.dumps(resize_img.tolist())}
    time_statistics.add_exec_time()

    result["time_statistics"] = time_statistics.to_list()
    result["start_time"] = 1000 * time.time()

    return result


if __name__ == '__main__':
    data_dir = "app/data"
    main({})
