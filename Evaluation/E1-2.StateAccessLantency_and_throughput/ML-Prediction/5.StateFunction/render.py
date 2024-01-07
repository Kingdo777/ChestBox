import json
import os
import numpy as np
import pickle
from tool import TimeStatistics
import ipc

os.environ['STATE_FUNCTION_LOG_LEVEL'] = 'off'
import statefunction as sf

data_dir = "/app/data"

Action_Pipe_Key = 0x1113


def render():
    time_statistics = TimeStatistics()
    ######################################################################
    time_statistics.dot()
    msg = ipc.create_msg(Action_Pipe_Key)
    bucket = sf.get_bucket("kingdo", True, Action_Pipe_Key)
    time_statistics.add_invoke_time()

    ######################################################################
    time_statistics.dot()
    x = pickle.loads(bucket.get_bytes("x"))
    time_statistics.add_access_time()

    ######################################################################
    time_statistics.dot()
    bucket.destroy()
    msg.destroy()
    time_statistics.add_invoke_time()

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
