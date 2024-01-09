import os
import subprocess
from os.path import dirname
import subprocess
import docker


def workflow():
    app_dir = os.path.join(dirname(os.path.abspath(__file__)), "app")
    # docker run --rm -v ./app:/app -w /app --ipc="container:state-function" \
    # kingdo/python-runtime python3 __main__.py
    container = docker.from_env().containers.run(image="kingdo/python-runtime",
                                                 volumes=[f'{app_dir}:/app'],
                                                 working_dir="/app",
                                                 detach=True, tty=True, stdin_open=True, stdout=True,
                                                 ipc_mode="container:state-function",
                                                 command="python3 __main__.py",
                                                 mem_limit="512m",
                                                 cpu_period=100000,
                                                 cpu_quota=100000
                                                 )
    container.wait()
    # print(container.logs().decode('utf-8').strip())
    result = list(map(float, container.logs().decode('utf-8').strip().split(',')))
    container.remove(force=True)

    out = ",".join(map(lambda x: "{:.2f}".format(x), result))
    print(out)
    return out


def run_predict(loop):
    subprocess.call("sudo rm -rf app", shell=True)
    subprocess.call("./gen-faastlane-runner.sh", shell=True)
    subprocess.call("cp -af ../data .faastlane/", shell=True)
    subprocess.call("cp -af ../nltk_data .faastlane/", shell=True)
    subprocess.call("mkdir app", shell=True)
    subprocess.call("cp -af .faastlane/* app/", shell=True)

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
