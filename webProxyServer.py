import socket
import os

HOST = "localhost"
PORT = 9000

proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy.bind((HOST,PORT))
proxy.listen();

print(f"Proxy listening on {HOST}:{PORT}")

while True:
    clientSocket, clientAddr = proxy.accept()
    request = clientSocket.recv(4096)
    print(request.decode)
    destinationHost = HOST
    destinationPort = 8080
    
    print(f"Request coming in to proxy is: \r\n {request}")
    # split the request up into parts
    requestLine = request.decode().split("\r\n")[0]
    parts = requestLine.split()
    requestFile = parts[1]
    cachePath = "cache" + requestFile
    if os.path.isfile(cachePath):
        print("This file exists, send it from here")
    else:
        print("This file does not exist, ask the web server")

    serverSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serverSocket.connect((destinationHost, destinationPort))

    serverSocket.sendall(request)

    response = serverSocket.recv(4096)

    clientSocket.sendall(response)

    serverSocket.close()
    clientSocket.close()

