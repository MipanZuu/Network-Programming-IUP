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

def clientthread(conn, addr, username):
    while True:
        try:
            message = str(conn.recv(2048).decode())
            if message.strip() == 'list':
                listallUsernames(conn)
            
            elif message.startswith('private'):
                privateMessage(message, username)

            elif message:
                    print('<' + username + '>' + message)
                    message_to_send = '<' + username + '> ' + message
                    broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)
                
def remove(connection):
    if connection in list_of_clients:
        username = username_list[list_of_clients.index(connection)]
        username_list.remove(username)
        list_of_clients.remove(connection)

def listallUsernames(conn):
    list_message = ""
    for username in username_list:
        list_message += username + '\n'
    conn.send(list_message.encode())

def privateMessage(message, username):
    message = message.split(None, 1)[-1]
    priv_user = message.split()[0]
    message = message.split(None, 1)[-1]
    priv_conn = list_of_clients[username_list.index(priv_user)]
    message_to_send = '<Private message from ' + username + '> ' + message
    try:
        priv_conn.send(message_to_send.encode())
    except:
        priv_conn.close()
        remove(priv_conn)
    

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
