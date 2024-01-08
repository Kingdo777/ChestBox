import pickle
import time
import redis
from tool import TimeStatistics, redis_host


def mask_entities_in_message(message, entity_list):
    for entity in entity_list:
        message = message.replace(entity['Text'], '#' * len(entity['Text']))
    return message


def main():
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    redis_client = redis.Redis(
        host=redis_host,
        port=6379)
    time_statistics.add_invoke_time()

    ######################################################################
    time_statistics.dot()
    message_data = redis_client.get("message")
    time_statistics.add_access_time()

    ######################################################################
    time_statistics.dot()
    message = pickle.loads(message_data)
    masked_message = mask_entities_in_message(message["message"], message["entities"])
    masked_message = pickle.dumps(masked_message)
    time_statistics.add_exec_time()

    ######################################################################
    time_statistics.dot()
    redis_client.set("masked_message", masked_message)
    time_statistics.add_access_time()

    print(time_statistics)


if __name__ == "__main__":
    main()
