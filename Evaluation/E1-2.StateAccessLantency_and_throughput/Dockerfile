FROM kingdo/state-function

RUN pip3 install --proxy=http://222.20.68.152:7890 tensorflow==2.10.0 pillow==9.4.0 numpy==1.24.2

RUN pip3 install --proxy=http://222.20.68.152:7890 redis

WORKDIR /app

CMD ["/bin/bash"]