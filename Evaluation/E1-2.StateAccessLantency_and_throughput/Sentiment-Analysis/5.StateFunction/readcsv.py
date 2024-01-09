import csv
import os
import pickle
import ipc

os.environ['STATE_FUNCTION_LOG_LEVEL'] = 'off'
import statefunction as sf

from tool import TimeStatistics

Action_Pipe_Key = 0x1111


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

    #####################################################################
    time_statistics.dot()
    msg = ipc.create_msg(Action_Pipe_Key)
    bucket = sf.create_bucket("kingdo", 1024 * 1024 * 4, True, Action_Pipe_Key)
    msg.destroy()
    time_statistics.add_invoke_time()

    ######################################################################
    time_statistics.dot()
    bucket.set("body_list", data)
    # print(size := len(data))
    time_statistics.add_access_time()

    print(time_statistics)


if __name__ == "__main__":
    main()
