import socket
import sys

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

sys.stdout.write('>> ')

try:
    while True:
        filename = str(input('Input filename for the content to be send: '))
        message = ""
        with open(filename) as f:
            contents = f.read()
            message =  message + contents
        f.close()
        client_socket.send(message.encode())
        sys.stdout.write(str(client_socket.recv(1024).decode()))
        sys.stdout.write('\n>> ')

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)