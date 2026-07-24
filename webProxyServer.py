import socket

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
    destinationHost = ...
    destinationPort = 80

    serverSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serverSocket.connect((destinationHost, destinationPort))

    serverSocket.sendall(request)

    response = ...

    clientSocket.sendall(responseO)

    serverSocket.close()
    clientSocket.close

