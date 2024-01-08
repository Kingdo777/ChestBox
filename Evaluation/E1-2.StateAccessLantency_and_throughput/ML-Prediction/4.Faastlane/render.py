import json
import os

import numpy as np

from tool import TimeStatistics

data_dir = "/app/data"


def main(event):
    time_statistics = TimeStatistics().from_list(event["time_statistics"])
    ######################################################################
    data = event["x"]
    time_statistics.add_access_time(event["start_time"])

    ######################################################################
    time_statistics.dot()
    x = np.array(json.loads(data))
    labels = json.load(open(os.path.join(data_dir, 'labels.json')))
    text = ("Top 1 Prediction: index({}), class({}), probability({})".
            format(x.argmax(), labels[str(x.argmax())], x.max()))
    time_statistics.add_exec_time()

    return str(time_statistics)
