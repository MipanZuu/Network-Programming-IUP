import socket 
import sys
import os

server_address = ('127.0.0.1', 5000)
client_socket = socket. socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(server_address) 

def SystemInterrupt():
    client_socket.close()
    sys.exit(0)

buf = 1024

try:
    filename = str(input('Input filename to be send: '))
    filesize = int(os.path.getsize(filename))
    client_socket.send(str(filesize).encode())
    with open(filename, 'rb') as f:
        while True:
            try:
                data = f.read(1024)
                if not data:
                    break
                client_socket.send(data)
            except KeyboardInterrupt:
                SystemInterrupt()
        
    while True:
        try:
            percentage = float(client_socket.recv(1024).decode())
            print('Server received ' + str(percentage) + '%% of the file')
        except socket.timeout:
            print ('Server is down') 
        else:
            break
        
except KeyboardInterrupt:
    SystemInterrupt()
    