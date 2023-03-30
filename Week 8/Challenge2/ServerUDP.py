import socket
import sys
import os

server_address = ('127.0.0.1', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address) 

def ServerInterupt():
    print('Server is interrupted')
    server_socket.shutdown(socket.SHUT_RDWR)
    server_socket.close()
    sys.exit(0)

filenamestart = 'receivedfile_'
filecount = 0
          
while True:
    try:
        filecount += 1
        filename = filenamestart + str(filecount) + '.txt'
        
        server_socket.settimeout(None)
        while True:
            try:
                data, client_address = server_socket.recvfrom(1024)
                if data:
                    break  
            except KeyboardInterrupt:
                ServerInterupt()
                
        actual_filesize = int(data.decode())
        number_of_blocks = int(actual_filesize / 1024)
        supposed_current_block = 0
        print('number of blocks: ', number_of_blocks)
        
        
        server_socket.settimeout(1)
        with open(filename, 'wb') as f:
            while True:
                try: 
                    supposed_current_block += 1
                    received_block = int(server_socket.recv(1024).decode())
                    print ('current block:', supposed_current_block , end="\r")
                    
                    if supposed_current_block != received_block:
                        failed_message = "Failed to receive block " + str(supposed_current_block)
                        server_socket.sendto(failed_message.encode(), client_address)
                    
                    data = server_socket.recv(1024)
                    
                    ack_message = "ack block " + str(supposed_current_block)
                    server_socket.sendto(ack_message.encode(), client_address)
                    
                    
                except socket.timeout:
                    failed_message = "Failed to receive block " + str(supposed_current_block)
                    server_socket.sendto(failed_message.encode(), client_address)
                except KeyboardInterrupt:
                    ServerInterupt()
                else:
                    f.write(data)
                    if supposed_current_block == number_of_blocks:
                        print('All blocks received')
                        break
            
        received_filesize = int(os.path.getsize(filename))
        percentage = (received_filesize / actual_filesize) * 100
        print('Finished receiving from ' + str(client_address) + ' from socket ' + str(server_socket.getsockname()))
        print('received ' + str(percentage) + '% of the file from sender.')
        server_socket.sendto(str(percentage).encode(), client_address)
        print('')
        continue

    except KeyboardInterrupt:
        ServerInterupt()