import socket 
import select 
import sys
import threading

server = socket.socket (socket.AF_INET, socket. SOCK_STREAM)
server.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 8081
server.bind((ip_address, port))
server.listen(100)
list_of_clients = []
username_list = []
assigned_group_list = []
group_list = []

def clientthread(conn, addr, username):
    assigned_group = groupPrompt(username,conn)
    print(assigned_group)

    while True:
        try:
            message = str(conn.recv(2048).decode())
            if message:
                    print('<' + username + '>' + message)
                    message_to_send = '<' + username + '> ' + message
                    broadcast(message_to_send, conn, assigned_group)
            else:
                remove(conn)
        except:
            continue

def broadcast(message, connection, assigned_group):
    for index, clients in enumerate(list_of_clients):
        if clients != connection and assigned_group == assigned_group_list[index]:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)
                
def remove(connection):
    if connection in list_of_clients:
        index = list_of_clients.index(connection)
        del username_list[index]
        del assigned_group_list[index]
        list_of_clients.remove(connection)

def groupPrompt(username ,conn):

    if len(group_list):
        list_group = 'Welcome to Denta-Fatih Chat System! Below are some groups you can join:\n\n'
        for group in group_list:
            list_group += group + '\n'
        list_group += '\n to join just type in the group name, or to create a new group just type new group name to create one!\n\n'
    else:
        list_group = 'Welcome to Denta-Fatih Chat System! Below are some groups you can join:\n\n there are no group available!\n\n To create a new group just type new group name to create one!\n\n'
    conn.send(list_group.encode())

    group_input = str(conn.recv(2048).decode())

    if group_input.startswith('new'):
        group_input = group_input.split(None, 1)[-1]
        if group_input not in group_list:
            group_list.append(group_input)
            print('new group '+ group_input + ' created!')
    assigned_group_list.append(group_input)
    print(username+ ' joined '+ group_input)
    return group_input

    

try:
    while True:
        conn, addr = server.accept()
        list_of_clients.append(conn)
        username = conn.recv(2048).decode()
        username_list.append(username)
        print(username + ' connected')
        threading.Thread(target=clientthread, args=(conn, addr, username)).start()
        
except KeyboardInterrupt:
    conn.close()
    sys.exit(0)
