import socket
import os

HOST = "localhost"
PORT = 8080

def createResponse(itemRequest):
    #Code 200 OK
    #Code 304 Not Modified
    #Code 403 Forbidden
    #Code 404 Not Found
    #Code 505 HTTP Version not supported
    printf(f"Item request is {itemRequest}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

print(f"Listening on {HOST}: {PORT}")
while True:
    clientSocket, clientAddr = server.accept()
    print("Connection Recieved")
    request = clientSocket.recv(4096).decode()
    requestLine = request.split("\r\n")[0]
    parts = requestLine.split()
    requestFile = parts[1]
    webServerPath = "webServer" + requestFile
    if os.path.isfile(webServerPath):
        with open(webServerPath, "rb") as file:
            response = file.read()
            response += b"\r\n Sent from the Web Server"

    else:
        print("Error")

    clientSocket.sendall(response)
    clientSocket.close()
