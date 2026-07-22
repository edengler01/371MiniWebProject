import socket
from _thread import start_new_thread
import threading


#reference  https://www.geeksforgeeks.org/python/socket-programming-multi-threading-python/
lock = threading.Lock()

def createResponse(itemRequest):
    #Code 200 OK
    #Code 304 Not Modified
    #Code 403 Forbidden
    #Code 404 Not Found
    #Code 505 HTTP Version not supported
    print(f"Item request is {itemRequest}")


'''
handle client requests

Request Template
--------------------
request line\r\n
header lines\r\n
\r\n
payload (might not have)
---------------------

    -request line: *method *file *HTTP version
    -header lines:
    -pay load: (might not have)
'''
def handle_client(clientSocket):
    while True:
        request = clientSocket.recv(4096).decode()
        if not request:
            lock.release()
            break

        # parse payout out of request
        parsedRequest = request.split('\r\n\r\n')

        if len(parsedRequest) > 1:
            payload = parsedRequest[1]

        # parse each line of request
        linesRequest = parsedRequest.split('\r\n')
        # Request line
        requestLine = linesRequest[0].split(' ')
        # header lines
        headerLines = linesRequest[1:]
        # determine which method is being requested
        match requestLine[0]:
            case "GET":
                print("GET")
            case "POST":
                print("POST")
            case "HEAD":
                print("HEAD")
            case "PUT":
                print("PUT")
            case "DELETE":
                print("DELETE")

        
        #what the client is trying to get
        print(linesRequest[1])




        #create a response and send it to the client
        #check the request and formulate the correct response
        clientSocket.send("test")
    clientSocket.close()

def main():
    HOST = ''
    PORT = 8081

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST,PORT))

    server.listen(5)

    print(f"Listening on {HOST}: {PORT}")
    while True:
        clientSocket, clientAddr = server.accept()

        lock.acquire()
        start_new_thread(handle_client, (clientSocket,))
        


if __name__ == '__main__':
    main()