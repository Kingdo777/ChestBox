import nltk
from tool import TimeStatistics

nltk.data.path.append('/app/nltk_data/')
from nltk.tokenize import word_tokenize


def main(event):
    time_statistics = TimeStatistics().from_list(event["time_statistics"])
    ######################################################################
    masked_message = event["masked_message"]
    time_statistics.add_access_time(event["start_time"])

    ######################################################################
    time_statistics.dot()
    tokens = word_tokenize(masked_message)
    time_statistics.add_exec_time()

    return str(time_statistics)
