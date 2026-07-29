import socket

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

    request = clientSocket.recv(4096).decode()
    print(f"Request Recieved \r\n {request}")

    # read and store HTML file contents
    with open("test.html", "rb") as file:
        htmlData = file.read()

    # create response header, hardcoded
    responseHeader = (
            "HTTP/1.1 200 OK \r\n"
            "Content-Type: text/html \r\n"
            f"Content-Length: {len(htmlData)}\r\n"
            "Connection: close \r\n"
            ).encode("utf-8")

   # combine data from html file to response header 
    clientSocket.sendall(responseHeader + htmlData)

