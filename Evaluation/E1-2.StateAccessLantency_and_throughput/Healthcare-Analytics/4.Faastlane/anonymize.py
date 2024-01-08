import json
import time

from tool import TimeStatistics


def mask_entities_in_message(message, entity_list):
    for entity in entity_list:
        message = message.replace(entity['Text'], '#' * len(entity['Text']))
    return message


def main(event):
    time_statistics = TimeStatistics().from_list(event["time_statistics"])
    ######################################################################
    data = event["data"]
    time_statistics.add_access_time(event["start_time"])

    ######################################################################
    time_statistics.dot()
    message = json.loads(data)
    masked_message = mask_entities_in_message(message["message"], message["entities"])
    result = {"masked_message": masked_message}
    time_statistics.add_exec_time()

    result["time_statistics"] = time_statistics.to_list()
    result["start_time"] = 1000 * time.time()

    return result


if __name__ == "__main__":
    main({})
