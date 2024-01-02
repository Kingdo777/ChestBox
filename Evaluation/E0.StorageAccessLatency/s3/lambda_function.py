import boto3
import time
import json

from botocore.config import Config

BUCKET = 'kingdo-chestbox'
File_KEY = 's3-bandwidth-latency/{}'

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_KEY_ID = ""
S3_REGION_NAME = "us-west-2"


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

    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_KEY_ID,
                      region_name=S3_REGION_NAME, )

    if op == "set":
        start_time = time.time()
        s3.put_object(Bucket=BUCKET, Key=File_KEY.format("data"), Body=data)
        write_use_time = (time.time() - start_time) * 1000
        print("write use {:.2f} ms".format(write_use_time))
        return {
            'statusCode': 200,
            'body': json.dumps({"set": "{:.3f}".format(write_use_time)})
        }

    elif op == "get":
        start_time = time.time()
        data = s3.get_object(Bucket=BUCKET, Key=File_KEY.format("data"))['Body'].read()
        read_use_time = (time.time() - start_time) * 1000
        print("read use {:.2f} ms".format(read_use_time))
        return {
            'statusCode': 200,
            'body': json.dumps({"get": "{:.3f}".format(read_use_time)})
        }
