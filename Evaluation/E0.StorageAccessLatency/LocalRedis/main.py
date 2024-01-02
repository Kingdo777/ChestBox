import sys
import redis
import tools

redis_client = redis.Redis(
    host="127.0.0.1",
    port=6379)


def main(size_s: str, option: str = "get"):
    data = b'A' * tools.s_to_size(size_s)

    if option == "set":
        tools.set_date(redis_client, data, size_s)
    elif option == "get":
        result = tools.get_date(redis_client, size_s)
        if result != data:
            return "NG"

    return "OK"


if __name__ == "__main__":
    main(size_s=sys.argv[1], option=sys.argv[2])
