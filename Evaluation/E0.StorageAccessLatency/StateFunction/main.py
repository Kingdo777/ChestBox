import os
from os.path import dirname
import subprocess
import sys
import time
import docker
import ipc
import statefunction as sf
import Evaluation.storage_access_latency.tools as tools

venv_path = os.path.join(dirname(dirname(dirname(os.getcwd()))), "venv")
Action_Pipe_Key = 0x11111
bucket: sf.Bucket


def main(size_s: str):
    data = b'A' * tools.s_to_size(size_s)

    tools.set_date(bucket, data, size_s)
    result = tools.get_date(bucket, size_s)

    if result is None:
        return "Failed"
    else:
        return "OK"


def join_docker_namespace(size_s):
    # docker inspect -f '{{.State.Pid}}' <container_id_or_name>
    container_pid = docker.from_env().api.inspect_container("state-function")['State']['Pid']
    subprocess.run(['nsenter', '--target', f"{container_pid}", '--ipc',
                    '--', os.path.join(venv_path, "bin/python3"), sys.argv[0], 'run', size_s])


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == "run":
        msg: ipc.MessageQueue = ipc.create_msg(Action_Pipe_Key)
        bucket = sf.create_bucket("kingdo", 1024 * 1024 * 128, True, Action_Pipe_Key)
        main(sys.argv[2])
        bucket.destroy()
        msg.destroy()
    else:
        join_docker_namespace("1KB" if len(sys.argv) != 2 else sys.argv[1])
