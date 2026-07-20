import socket

HOST = "172.16.85.93"
PORT = 8081

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
    parsedRequest = request.split('\r\n')

    #HTTP Get
    print(parsedRequest[0])
    #what the client is trying to get
    print(parsedRequest[1])




    #create a response and send it to the client
    #check the request and formulate the correct response
    clientSocket.send("test")

