import struct
import time

anonymize_server_port = 8080
analytics_server_port = 8081


class TimeStatistics:
    def __init__(self):
        self.exec_time = 0
        self.invoke_time = 0
        self.access_time = 0
        self.resides_time = 0
        self.start_time = 1000 * time.time()

    def dot(self):
        self.start_time = 1000 * time.time()

    def add_exec_time(self):
        self.exec_time += (1000 * time.time() - self.start_time)

    def add_invoke_time(self):
        self.invoke_time += (1000 * time.time() - self.start_time)

    def add_access_time(self):
        self.access_time += (1000 * time.time() - self.start_time)

    def add_resides_time(self, start_time):
        self.resides_time += (1000 * time.time() - start_time)

    def reset(self):
        self.exec_time = 0
        self.invoke_time = 0
        self.access_time = 0
        self.resides_time = 0

    def __str__(self):
        return "{:.2f},{:.2f},{:.2f},{:.2f}".format(
            self.exec_time, self.invoke_time, self.access_time, self.resides_time)

    def to_list(self) -> list:
        return [self.exec_time, self.invoke_time, self.access_time, self.resides_time]


def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)
