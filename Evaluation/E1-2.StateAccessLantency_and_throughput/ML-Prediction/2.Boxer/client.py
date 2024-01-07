import socket
from tool import *

if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("222.20.94.67", 12345))
    message = b'A' * (1024 * 1024)
    start_time = time.time()
    send_msg(client_socket, message)
    print(f"Time elapsed: {(time.time() - start_time) * 1000} ms")
    client_socket.close()
