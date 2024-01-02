import json
import time
import redis

elasticache_config_endpoint = ""
target_port = 6379


def s_to_size(size_s: str):
    if size_s == "4KB":
        return 4 * 1024
    elif size_s == "1MB":
        return 1024 * 1024
    elif size_s == "10MB":
        return 10 * 1024 * 1024
    elif size_s == "100MB":
        return 100 * 1024 * 1024
    else:
        return 1024


def lambda_handler(event, context):
    body = json.loads(event["body"])
    size = s_to_size(body["size"])
    op = body["op"]
    data = b'A' * size

    redis_client = redis.Redis(
        host=elasticache_config_endpoint,
        port=target_port,
        ssl=True, )

    if op == "set":
        start_time = time.time()
        redis_client.set("data", data)
        write_use_time = (time.time() - start_time) * 1000
        print("write use {:.2f} ms".format(write_use_time))
        return {
            'statusCode': 200,
            'body': json.dumps({"set": "{:.3f}".format(write_use_time)})
        }
    elif op == "get":
        start_time = time.time()
        result = redis_client.get("data")
        read_use_time = (time.time() - start_time) * 1000
        print("read use {:.2f} ms".format(read_use_time))
        return {
            'statusCode': 200,
            'body': json.dumps({"get": "{:.3f}".format(read_use_time)})
        }
