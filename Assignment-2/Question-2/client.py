import socket

s = socket.socket()

port = 1235

s.connect(('172.16.19.24', port))

print(s.recv(1024).decode())
s.close()    