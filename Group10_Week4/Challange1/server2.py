#GROUP 10
# Denta Bramasta Hidayat - 5025201116
# Muhammad Fatih Akbar - 5025201117

import socket
import sys
from datetime import datetime

server_address = ('localhost', 5002)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(client_socket, client_address)
        
        data = client_socket.recv(1024).decode()

        print("Received data: " + str(data))
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        
        # Challenge 2 - No.2
        f = open("log.txt","a")
        log_content = "\n" + str(ts) + "\n" + str(client_socket) + "\n" + str(data)
        f.writelines(str(log_content))
        f.close()

        # Challenge 2 - No.4
        if(str(data) == "asklog"):
            print("asked for log.txt")
            f = open("log.txt","r")
            asklog_content = str(f.readlines())
            client_socket.send(asklog_content.encode())
        
        # Challenge 2 - No.3
        client_socket.send(log_content.encode())

        client_socket.close()
        
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)