import csv
import json
import time

from tool import TimeStatistics


def main(event):
    time_statistics = TimeStatistics()

    ######################################################################
    time_statistics.dot()
    body_list = []
    with open('/app/data/few_reviews.csv') as csvFile:
        # DictReader -> convert lines of CSV to OrderedDict
        for row in csv.DictReader(csvFile):
            # return just the first loop (row) results!
            body = {}
            for k, v in row.items():
                body[k] = int(v) if k == 'reviewType' else v
            body_list.append(body)
    result = {"data": json.dumps(body_list)}
    time_statistics.add_exec_time()

    result["time_statistics"] = time_statistics.to_list()
    result["start_time"] = 1000 * time.time()

    return result


if __name__ == '__main__':
    data_dir = "app/data"
    main({})
