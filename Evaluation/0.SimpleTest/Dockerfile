FROM ubuntu:22.04

# install zip && python3.10
RUN apt-get update && apt-get install -y python3.10 python3.10-dev python3-pip zip libcurl4-openssl-dev\
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install --proxy http://222.20.68.152:7890 -r /tmp/requirements.txt

COPY statefunction-3.0.0-cp310-cp310-linux_x86_64.whl /tmp/statefunction-3.0.0-cp310-cp310-linux_x86_64.whl
COPY ipc-1.0.0-cp310-cp310-linux_x86_64.whl /tmp/ipc-1.0.0-cp310-cp310-linux_x86_64.whl
RUN pip install /tmp/statefunction-3.0.0-cp310-cp310-linux_x86_64.whl /tmp/ipc-1.0.0-cp310-cp310-linux_x86_64.whl

COPY data /app/data

COPY main.py /app

WORKDIR /app

# turn off the state function spdlog
ENV STATE_FUNCTION_LOG_LEVEL="off"
# turn off the tensorflow log
ENV TF_CPP_MIN_LOG_LEVEL="3"


CMD ["python3", "main.py"]

