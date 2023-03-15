import socket
import select
import sys

def isPalindrome(s):
    rev = ''.join(reversed(s))
    if (s == rev):
        return str(s + " - Yes")
    else:
        return str(s + " - No")

server_address = ('127.0.0.1', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
            else:
                data = str(sock.recv(1024).decode())
                #print(data)
                result = ""
                for line in data.splitlines():
                    print(isPalindrome(line))
                    result = result + isPalindrome(line) + "\n"
                if str(result):
                    sock.send(result.encode())
                    resfile = open('result.txt', 'a')
                    resfile.writelines(result)
                    resfile.close()
                else:
                    sock.close()
                    input_socket.remove(sock)

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)