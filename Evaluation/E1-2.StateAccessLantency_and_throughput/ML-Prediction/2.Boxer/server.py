import socket
from tool import *

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    while True:
        client_socket, addr = server_socket.accept()
        time_start = time.time()
        data = recv_msg(client_socket)
        print(f"Time elapsed: {(time.time() - time_start) * 1000} ms")
        client_socket.close()
