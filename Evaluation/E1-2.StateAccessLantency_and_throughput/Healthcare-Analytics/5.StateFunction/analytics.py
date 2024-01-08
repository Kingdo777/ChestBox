import nltk
import pickle
import ipc
import os

os.environ['STATE_FUNCTION_LOG_LEVEL'] = 'off'
import statefunction as sf
from tool import TimeStatistics

nltk.data.path.append('/app/nltk_data/')
from nltk.tokenize import word_tokenize

Action_Pipe_Key = 0x1113


def main():
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    msg = ipc.create_msg(Action_Pipe_Key)
    bucket = sf.get_bucket("kingdo", True, Action_Pipe_Key)
    time_statistics.add_invoke_time()

    ######################################################################
    time_statistics.dot()
    masked_message = bucket.get("masked_message")
    bucket.destroy()
    msg.destroy()
    time_statistics.add_access_time()

    ######################################################################
    time_statistics.dot()
    tokens = word_tokenize(masked_message)
    time_statistics.add_exec_time()

    # print(tokens)
    print(time_statistics)


if __name__ == '__main__':
    main()
