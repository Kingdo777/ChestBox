import os
import subprocess
from os.path import dirname
import subprocess
import docker


def workflow():
    subprocess.call("sudo rm -rf app", shell=True)
    subprocess.call("mkdir app", shell=True)
    subprocess.call("cp ./*py app", shell=True)
    subprocess.call("cp -af ../data app/", shell=True)

    commands = ["python3 resize.py", "python3 predict.py", "python3 render.py"]
    mem_limits = ["128m", "1g", "128m"]
    results = []

    app_dir = os.path.join(dirname(os.path.abspath(__file__)), "app")

    for i in range(3):
        container = docker.from_env().containers.run(image="kingdo/python-runtime",
                                                     volumes=[
                                                         f'{app_dir}:/app'],
                                                     working_dir="/app",
                                                     detach=True, tty=True, stdin_open=True, stdout=True,
                                                     command=commands[i],
                                                     mem_limit=mem_limits[i],
                                                     cpu_period=100000,
                                                     cpu_quota=100000,
                                                     network="host")
        container.wait()
        # print(container.logs().decode('utf-8').strip())
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
    results = []
    for i in range(loop):
        results.append(workflow())
    return results


def main(loop: int = 1):
    try:
        result = run_predict(loop)
        record_file = "results/summary"
        with open(record_file, "w") as f:
            f.write("exec_time,invoke_time,access_time,resides_time\n")
            for i in result:
                f.write(str(i) + "\n")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # try:
    #     # docker stop state-function
    #     docker.from_env().api.stop("redis-server")
    #     print("stop old redis-server container")
    # except Exception as e:
    #     print(e)
    #
    # try:
    #     # docker run -d --rm -p 6379:6379 --name redis-server redis
    #     docker.from_env().containers.run("redis", detach=True, ports={'6379/tcp': 6379},
    #                                      name="redis-server", remove=True)
    #
    #     print("start new redis-server container")
    # except Exception as e:
    #     print(e)
    #     exit(0)

    main(1)
