import os
import pickle
from tool import TimeStatistics
import ipc

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

os.environ['STATE_FUNCTION_LOG_LEVEL'] = 'off'
import statefunction as sf

data_dir = "/app/data"

Action_Pipe_Key = 0x1112


def predict():
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    msg = ipc.create_msg(Action_Pipe_Key)
    bucket = sf.get_bucket("kingdo", True, Action_Pipe_Key)
    msg.destroy()
    time_statistics.add_invoke_time()

    ######################################################################
    time_statistics.dot()
    resize_img = bucket.get_bytes("resize_img")
    time_statistics.add_access_time()

    ######################################################################
    time_statistics.dot()
    gd = tf.compat.v1.GraphDef. \
        FromString(open(os.path.join(data_dir, 'mobilenet_v2_1.0_224_frozen.pb'), 'rb').read())
    inp, predictions = tf. \
        import_graph_def(gd, return_elements=['input:0', 'MobilenetV2/Predictions/Reshape_1:0'])
    with tf.compat.v1.Session(graph=inp.graph):
        x = pickle.dumps(predictions.eval(feed_dict={inp: pickle.loads(resize_img)}))
    time_statistics.add_exec_time()

    ######################################################################
    time_statistics.dot()
    bucket.set("x", x)
    time_statistics.add_access_time()

    print(time_statistics)


if __name__ == '__main__':
    predict()
