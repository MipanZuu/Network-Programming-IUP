import socket
import sys

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

sys.stdout.write('>> ')

try:
    while True:
        message = str(input())
        client_socket.send(message.encode())
        sys.stdout.write(client_socket.recv(1024).decode())
        sys.stdout.write('\n' + '>> ')

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)