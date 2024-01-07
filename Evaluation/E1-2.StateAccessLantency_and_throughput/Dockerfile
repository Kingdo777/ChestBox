FROM python:3.10
LABEL authors="kingdo"

RUN pip3 install --proxy=http://222.20.68.152:7890 tensorflow==2.10.0 pillow==9.4.0 numpy==1.24.2

RUN pip3 install --proxy=http://222.20.68.152:7890 redis

RUN pip3 install --proxy=http://222.20.68.152:7890 stun

WORKDIR /app

CMD ["/bin/bash"]