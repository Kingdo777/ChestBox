import nltk
import pickle
import redis
from tool import TimeStatistics, redis_host

nltk.data.path.append('/app/nltk_data/')
from nltk.tokenize import word_tokenize


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
    masked_message = redis_client.get("masked_message")
    time_statistics.add_access_time()

    ######################################################################
    time_statistics.dot()
    masked_message = pickle.loads(masked_message)
    tokens = word_tokenize(masked_message)
    time_statistics.add_exec_time()

    # print(tokens)
    print(time_statistics)


if __name__ == '__main__':
    main()
