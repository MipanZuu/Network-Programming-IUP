import socket
import threading
import sys
import os

script_dir = os.path.dirname(__file__)

server_address = ('localhost', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)


def recv_msg():

    while True:
        print('')
        recv_msg = str(client_socket.recv(1024).decode())

        if len(recv_msg.splitlines()) > 1:
            print(recv_msg.splitlines()[0])
            newfile = open(os.path.join(script_dir, recv_msg.splitlines()[1]), 'w')
            recv_msg = recv_msg.split("\n",2)[2]
            newfile.write(recv_msg)
            newfile.close()
            print('Input filename for the content to be send: ')
        else:
            print(recv_msg)
            print('Input filename for the content to be send: ')

        if not recv_msg:
            sys.exit(0)

def send_msg():
    try:
        while True:
            filename = str(input('Input filename for the content to be send: '))
            message = filename + "\n"
            with open(os.path.join(script_dir, filename)) as f:
                contents = f.read()
                #print(str(contents))
                message =  message + contents
            f.close()
            client_socket.send(message.encode())
    except KeyboardInterrupt:
        client_socket.close()
        sys.exit(0)


t = threading.Thread(target=recv_msg)
t.start()
send_msg()
