import os
import subprocess
import time
from os.path import dirname

from tool import anonymize_server_port, analytics_server_port

import docker


def run_container(command, memory_limit) -> docker.DockerClient:
    app_dir = os.path.join(dirname(os.path.abspath(__file__)), "app")
    container_name = command.removeprefix("python3 ").removesuffix(".py") + "-boxer"
    subprocess.call(f"docker stop {container_name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call(f"docker rm {container_name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if container_name == "anonymize-boxer":
        ports = {f"{anonymize_server_port}/tcp": anonymize_server_port}
    elif container_name == "analytics-boxer":
        ports = {f"{analytics_server_port}/tcp": analytics_server_port}
    else:
        ports = None

    # docker run --name anonymize -v ./app:/app -it --rm --network=host kingdo/python-runtime python3 anonymize.py
    return docker.from_env().containers.run(image="kingdo/python-runtime",
                                            name=container_name,
                                            volumes=[f'{app_dir}:/app'],
                                            working_dir="/app",
                                            detach=True, stdin_open=True, stdout=True,
                                            ports=ports,
                                            command=command,
                                            mem_limit=memory_limit,
                                            cpu_period=100000,
                                            cpu_quota=100000)


def workflow():
    subprocess.call("sudo rm -rf app", shell=True)
    subprocess.call("mkdir app", shell=True)
    subprocess.call("cp ./*py app", shell=True)
    subprocess.call("cp -af ../nltk_data app/", shell=True)

    results = []

    anonymize_container = run_container("python3 anonymize.py", "128m")
    time.sleep(3)
    analytics_container = run_container("python3 analytics.py", "128m")
    time.sleep(3)
    identifyphi_container = run_container("python3 identifyphi.py", "128m")

    container_list = [identifyphi_container, anonymize_container, analytics_container]

    for container in container_list:
        container.wait()
        # print(container.logs().decode('utf-8'))
        results.append(list(map(float, container.logs().decode('utf-8').strip().split(','))))
        container.remove(force=True)

    summary = [0.0 for _ in range(len(results[0]))]
    for result in results:
        for i in range(len(result)):
            summary[i] += result[i]

    out = ",".join(map(lambda x: "{:.2f}".format(x), summary))
    print(out)
    return out


def run_workflow(loop):
    results = []
    for i in range(loop):
        results.append(workflow())
    return results


def main(loop: int = 1):
    try:
        result = run_workflow(loop)
        record_file = "results/summary"
        with open(record_file, "w") as f:
            f.write("exec_time,invoke_time,access_time,resides_time\n")
            for i in result:
                f.write(str(i) + "\n")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main(100)
