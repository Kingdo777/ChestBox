import json
import time
import ssl
from pymemcache.client.base import Client

elasticache_config_endpoint = ""
target_port = 11211

tls_context = ssl.create_default_context()

memcached_client = Client((elasticache_config_endpoint, target_port), tls_context=tls_context)


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
    body = event["body"]
    # size = s_to_size(body["size"])
    size = s_to_size(json.loads(body)["size"])
    data = b'A' * size

    start_time = time.time()
    memcached_client.set("data", data, expire=500, noreply=False)
    write_use_time = (time.time() - start_time) * 1000
    print("write use {:.2f} ms".format(write_use_time))

    start_time = time.time()
    result = memcached_client.get("data")
    read_use_time = (time.time() - start_time) * 1000
    print("read use {:.2f} ms".format(read_use_time))

    result = {
        "write": "{:.3f}".format(write_use_time),
        "read": "{:.3f}".format(read_use_time)
    }

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
