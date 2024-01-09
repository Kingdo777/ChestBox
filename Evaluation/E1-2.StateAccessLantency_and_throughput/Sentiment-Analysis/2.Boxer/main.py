import os
import time
from os.path import dirname
import subprocess
import docker

from tool import sentiment_server_port, WritetoDB_server_port, publishsns_server_port


def run_container(command, memory_limit) -> docker.DockerClient:
    app_dir = os.path.join(dirname(os.path.abspath(__file__)), "app")
    container_name = command.removeprefix("python3 ").removesuffix(".py") + "-boxer"
    subprocess.call(f"docker stop {container_name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call(f"docker rm {container_name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if container_name == "sentiment-boxer":
        ports = {f"{sentiment_server_port}/tcp": sentiment_server_port}
    elif container_name == "WritetoDB-boxer":
        ports = {f"{WritetoDB_server_port}/tcp": WritetoDB_server_port}
    elif container_name == "publishsns-boxer":
        ports = {f"{publishsns_server_port}/tcp": publishsns_server_port}
    else:
        ports = None

    # docker run --name predict -v ./app:/app -it --rm --network=host kingdo/python-runtime python3 predict.py
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
    commands = ["python3 readcsv.py", "python3 sentiment.py", "python3 WritetoDB.py", "python3 publishsns.py"]
    mem_limits = ["128m", "512m", "128m", "128m"]
    results = []

    sentiment_container = run_container("python3 sentiment.py", "512m")
    time.sleep(3)
    WritetoDB_container = run_container("python3 WritetoDB.py", "128m")
    time.sleep(3)
    publishsns_container = run_container("python3 publishsns.py", "128m")
    time.sleep(3)
    readcsv_container = run_container("python3 readcsv.py", "128m")

    container_list = [readcsv_container, sentiment_container, WritetoDB_container, publishsns_container, ]

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


def run_predict(loop):
    subprocess.call("sudo rm -rf app", shell=True)
    subprocess.call("mkdir app", shell=True)
    subprocess.call("cp ./*py app", shell=True)
    subprocess.call("cp -af ../nltk_data app/", shell=True)
    subprocess.call("cp -af ../data app/", shell=True)
    results = []
    for i in range(loop):
        results.append(workflow())
    return results


def main(loop: int = 1):
    try:
        result = run_predict(loop)
        record_file = "results/summary"
        with open(record_file, "w") as f:
            for i in result:
                f.write(str(i) + "\n")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main(100)
