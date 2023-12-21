FROM ubuntu:22.04

# install zip && python3.10
RUN apt-get update && apt-get install -y python3.10 python3.10-dev python3-pip zip libcurl4-openssl-dev\
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install --proxy http://222.20.68.152:7890 -r /tmp/requirements.txt

COPY statefunction-3.0.0-cp310-cp310-linux_x86_64.whl /tmp/statefunction-3.0.0-cp310-cp310-linux_x86_64.whl
RUN pip install /tmp/statefunction-3.0.0-cp310-cp310-linux_x86_64.whl

COPY . /app

WORKDIR /app

CMD ["python3", "main.py"]

