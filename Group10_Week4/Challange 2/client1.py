#GROUP 10
# Denta Bramasta Hidayat - 5025201116
# Muhammad Fatih Akbar - 5025201117

import socket

# Challenge 2 - No.1 
serverIP = input("server IP: ")
serverPORT = input("server PORT: ")
message = input("enter message: ")

server_address = (str(serverIP), int(serverPORT))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)
client_socket.send(message.encode())

# Challenge 2 - No.4
if(str(message) == "asklog"):
    print("asking for log")
    data = client_socket.recv(1024).decode()
    print(str(data))

# Challenge 2 - No.2
data = client_socket.recv(1024).decode()
print(str(data))
    
client_socket.close()