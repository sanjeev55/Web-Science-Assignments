import socket

HOST = socket.gethostbyname(socket.gethostname()) #Finding local IP address
PORT = 10000        # port used by server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
    skt.connect((HOST, PORT)) #to connect to a remote server address
    data = skt.recv(1024) #reads at most 1024 bytes, blocks if no data

print(data)