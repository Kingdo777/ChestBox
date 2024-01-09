import csv
import pickle

import redis

from tool import TimeStatistics, redis_host


def main():
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
    data = pickle.dumps(body_list)
    time_statistics.add_exec_time()

    ######################################################################
    time_statistics.dot()
    redis_client = redis.Redis(host=redis_host, port=6379, db=0)
    time_statistics.add_invoke_time()

    ######################################################################
    time_statistics.dot()
    redis_client.set("body_list", data)
    time_statistics.add_access_time()

    print(time_statistics)


if __name__ == "__main__":
    main()
