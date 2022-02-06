import socket, time

host = '195.142.134.246'
port = 15001                   # The same port as used by the server
print(host)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
while True:
    s.sendall(b'65701')
    time.sleep(1)
s.close()

'''

'''