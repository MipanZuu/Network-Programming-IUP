import select
import socket
import sys
import threading

CLIENT_LIST = []

class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host,self.port))
        self.server.listen(5)

    def run(self):
        self.open_socket()
        input = [self.server]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:
                if s == self.server:
                    # handle the server socket
                    client_socket, client_address = self.server.accept()
                    c = Client(client_socket, client_address)
                    c.start()
                    self.threads.append(c)
                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

	 # close all threads
        self.server.close()
        for c in self.threads:
            c.join()

class Client(threading.Thread):
    number_of_clients = 0
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        Client.number_of_clients += 1
        CLIENT_LIST.append(self)
        self.number = Client.number_of_clients
        self.client_name = "Client " + str(self.number)

    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size).decode()
            # print(data)
            #print (str(self.address) + " " + self.client_name + " " + str(data))
            filename = str(data).partition('\n')[0]
            message = "Receiving file from " + self.client_name + ". Filename: " + filename + "\n" + str(data) 
            print(message)
            if data:
                for clients in CLIENT_LIST:
                    if clients.number != self.number:
                        clients.client.send(message.encode())

                self_message = "Message will be sent to "

                if Client.number_of_clients > 1:
                    for clients in CLIENT_LIST:
                        print(clients.client_name)
                        if clients.number != self.number:
                            self_message += "Client " + str(clients.number)
                            if clients.number == Client.number_of_clients:
                                self_message += "."
                            else:
                                self_message += " ,"
                else:
                    self_message += "no one."

                self.client.send(self_message.encode())
            else:
                self.client.close()
                running = 0

if __name__ == "__main__":
    s = Server()
    s.run()