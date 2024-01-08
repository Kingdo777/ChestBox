import pickle
import time
import redis
from tool import TimeStatistics
import ipc
import os

os.environ['STATE_FUNCTION_LOG_LEVEL'] = 'off'
import statefunction as sf

Action_Pipe_Key = 0x1112


def mask_entities_in_message(message, entity_list):
    for entity in entity_list:
        message = message.replace(entity['Text'], '#' * len(entity['Text']))
    return message


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
    message_data = bucket.get_bytes("message")
    time_statistics.add_access_time()

    ######################################################################
    time_statistics.dot()
    message = pickle.loads(message_data)
    masked_message = mask_entities_in_message(message["message"], message["entities"])
    time_statistics.add_exec_time()

    ######################################################################
    time_statistics.dot()
    bucket.set("masked_message", masked_message)
    time_statistics.add_access_time()

    print(time_statistics)


if __name__ == "__main__":
    main()
