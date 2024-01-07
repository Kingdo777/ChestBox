import os
import numpy as np
import pickle
from PIL import Image
from tool import TimeStatistics
import ipc

os.environ['STATE_FUNCTION_LOG_LEVEL'] = 'off'
import statefunction as sf

data_dir = "/app/data"

Action_Pipe_Key = 0x1111


def main():
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    image = Image.open(os.path.join(data_dir, 'panda.jpg'))
    img = np.array(image.resize((224, 224))).astype(float) / 128 - 1
    resize_img = pickle.dumps(img.reshape(1, 224, 224, 3))
    time_statistics.add_exec_time()

    ######################################################################
    time_statistics.dot()
    msg = ipc.create_msg(Action_Pipe_Key)
    bucket = sf.create_bucket("kingdo", 1024 * 1024 * 2, True, Action_Pipe_Key)
    msg.destroy()
    time_statistics.add_invoke_time()

    ######################################################################
    time_statistics.dot()
    bucket.set("resize_img", resize_img)
    time_statistics.add_access_time()

    print(time_statistics)


if __name__ == '__main__':
    main()
